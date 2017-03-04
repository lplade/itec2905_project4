#!/usr/bin/python3

from flask import Flask, render_template, request, flash, redirect, url_for, abort
from flask_googlemaps import GoogleMaps
import datetime
import logging
from werkzeug.contrib.cache import FileSystemCache
import bandsearch_api
import flightsearch_stub
import lodging_api
import maps_api
from secrets import *

# Sets the verbosity of console logging
logging.basicConfig(level=logging.DEBUG)

# any needed Flask configuration can be passed as arguments to this
app = Flask(__name__)

# Set up Flask-GoogleMaps
GoogleMaps(app, key=GOOGLE_MAPS_API_KEY)

# Set up Werkzeug's FileSystemCache
cache = FileSystemCache("./cache")
# TODO port to use Memcached server instead?


##########
# Helper functions
##########

def retrieve_full_event_list(band_name):
    # Catch-22 here... ideally, we store by (unique) id field.
    # We can't get the id field without doing a query first
    # For now, generate a key
    # This won't catch minor spelling/formatting variations
    cache_key = "band_{}".format(band_name)

    # FIRST, we should check our cache to see if we have these results saved
    event_list = cache.get(cache_key)

    # If it's not there, make API call
    if event_list is None:
        event_list = bandsearch_api.search_by_band(
            band_name=band_name
        )
        # cache for 1 hour
        cache.set(cache_key, event_list, timeout=60 * 60)
        # Note that we keep the UNfiltered results cached

    return event_list


def filter_event_list_by_distance(
        event_list, max_distance, start_city_latitude, start_city_longitude):

    # rebuild the list, filtering by distance
    new_list = []

    # go in and set the distance on each concert
    for concert in event_list:
        concert.set_distance_from_origin(
            origin_latitude=start_city_latitude,
            origin_longitude=start_city_longitude
        )
        if concert.distance <= max_distance:
            new_list.append(concert)

    # return a list that doesn't have distant entries
    return new_list


##########
# Routes
##########


@app.route('/', methods=["GET"])
def index():

    # display the main form

    return render_template("main.html")


@app.route('/bandsearch', methods=["POST"])
def band_search():
    # Do this stuff only if we are submitting the form
    if request.method == "POST":
        # First parse the input provided by the form
        band_query = str(request.form["band_query"])
        start_city = str(request.form["start_city"])
        max_distance = float(request.form["max_distance"])

        # Get the coordinates for the start city
        start_city_latitude, start_city_longitude = \
            maps_api.find_location_coordinates(start_city)
        # TODO asynchronous? callback?

        # Query the cache or the API
        event_list = retrieve_full_event_list(band_query)

        # replace the event list
        event_list = filter_event_list_by_distance(
            event_list, max_distance, start_city_latitude, start_city_longitude)

        # TODO query flight prices here?

        # FINALLY, we can return the results to user
        # TODO return proper band name from API call?
        total_results = len(event_list)

        # TODO do any other processing of the results in here

        return render_template("event_results.html",
                               event_list=event_list,
                               total_results=total_results,
                               band_name=band_query)
    else:
        # We should not access this route by GET, so redirect
        return redirect("/", code=302)


@app.route("/hotelsearch", methods=["POST"])
def hotel_search():
    if request.method == "POST":
        event_id = str(request.form["event_id"])
        band_name = str(request.form["band_name"])
        search_radius = int(request.form["search_radius"])
        cheap_limit = int(request.form["cheap_limit"])

        # And here is where we probably SHOULD have stored this in a real DB
        event_list = retrieve_full_event_list(band_name)

        # Loop over the WHOLE LIST of cached events to find the right event
        for concert in event_list:
            if concert.event_id == event_id:
                selected_concert = concert
                break

        try:  # make sure selected_concert just got set
            selected_concert
        except NameError:
            logging.error("Unable to retrieve previously retrieved event")
            abort(500)
        else:
            rs = lodging_api.get_query_lodging(
                city=selected_concert.city_name,
                state=selected_concert.region_name,
                country=selected_concert.country_name,
                radius=search_radius,
                cheap_limit=cheap_limit
            )

            return render_template(
                "hotel_search.html",
                event_id=event_id,
                band_name=band_name,
                search_radius=search_radius,
                cheap_limit=cheap_limit,
                concert=selected_concert,
                hotel_results=rs
            )

    else:
        # We should not access this route by GET, so redirect
        return redirect("/", code=302)


# Leave this as the last route
@app.route("/<path:path>")
def serve_static(path):
    """
    Assume any request not matching above routes is request for static resource
    :param path:
    :return:
    """
    return app.send_static_file(path)

#########
# Run application
#########

if __name__ == '__main__':
    app.run()
