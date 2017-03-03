#!/usr/bin/python3

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_googlemaps import GoogleMaps
import datetime
import concerts_bands_API
import lodging
from secrets import *

# any needed Flask configuration can be passed as arguments to this
app = Flask(__name__)

# We'll configure the SQLalchemy stuff here for the moment
# TODO split ORM stuff into its own file
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///musicfan.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # this squelches the
#                                                       console warning
db = SQLAlchemy(app)

# Set up Flask-GoogleMaps
GoogleMaps(app, key=GOOGLE_MAPS_API_KEY)

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

        # FIRST, we should check our cache to see if we have these results saved
        # TODO implement caching

        # IF WE DO, return that

        # OTHERWISE, make API call
        # TODO try-except this?
        event_list = concerts_bands_API.search_by_band(
            band_name=band_query,
            origin=start_city,
            max_distance=max_distance
        )

        # TODO query flight prices here?

        # DO SOMETHING to put this into cache?

        # FINALLY, we can return the results to user
        # TODO return proper band name from API call?
        total_results = len(event_list)

        # TODO do any other processing of the results in here

        # TODO figure out distance based on lat/long here?

        return render_template("event_results.html",
                               event_list=event_list,
                               total_results=total_results,
                               band_name=band_query)
    else:
        # We should not access this route by GET, so redirect
        return redirect("/", code=302)


@app.route("/hotelsearch", methods=["POST"])
def hotel_search():

    pass
    # TODO write this
    # rs = lodging.get_query_lodging(
    #     city=city,
    #     state=state,
    #     country=country,
    #     radius=radius,
    #     cheap_limit=cheap_limit
    # )


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
