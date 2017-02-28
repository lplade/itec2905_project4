import urllib.request
import urllib.parse
import requests
# import json

# This includes our secret API key
from secrets import *


class Concert:
    # data structure to store retrieved json data about a single event

    def __init__(self, title, date, region_name, city_name, country_name,
                 longitude, latitude):
        title = title
        date = date  # what format is this stored in?
        region_name = region_name  # State, in USA
        city_name = city_name
        country_name = country_name
        longitude = longitude
        latitude = latitude
        # TODO add venue_name and venue_address


def search_by_band(band_name, origin="Minneapolis, MN", max_distance=500):
    """

    :param band_name: name of artist we are searching for
    :param origin: city we are starting from
    :param max_distance: how far are we willing to travel
    :return: list of Concert
    """

    # The 'category' argument, also called 'c', is used to search within
    # a category.

    # We have to use .urlencode to properly encode spaces and such into ASCII
    # URL string
    params = urllib.parse.urlencode(({
        'q': band_name,
        'location': origin,
        'within': max_distance,
        'units': 'mi',
        'app_key': EVENTFUL_KEY
        # TODO add any other request parameters here
    }))
    # This builds the URL we need for our API request
    api_url = 'http://api.eventful.com/json/events/search?%s' % params

    # Get the data in a json format
    json_data = requests.get(api_url).json()

    # initialize an empty list
    event_list = []

    # First loop, gets the first keys, then it gets passed to the next one.
    for key, value in json_data['events'].items():
        # This loop has to be iter because is a list.

        for newValue in iter(value):
            # This loops each key and gets the value that it is needed
            for item in newValue:
                title = str(newValue['title'])
                state = str(newValue['region_name'])
                city = str(newValue['city_name'])
                country = str(newValue['country_name'])
                longitude = float(newValue['longitude'])
                latitude = float(newValue['latitude'])
                # TODO get venue_name and venue_address for hotels
                # TODO we need to get the event date too!
                # TODO url? I didn't think that the url is necessary because we need
                # the one for the hotels and travel options only.

                event_object = Concert(title=title,
                                       date=date,
                                       region_name=state,
                                       city_name=city,
                                       country_name=country,
                                       longitude=longitude,
                                       latitude=latitude)

                event_list.append(event_object)

    return event_list


def main():
    band = input("What band to search for? ")

    concert_list = search_by_band(band)

    # TODO simple interactive console test routine should go here
    # This will not be used in the final app

    # # This is to keep track  of the number of concerts.
    # counter = 0
    #
    # for concert in concert_list:
    #     counter += 1
    #
    #     # Print staments
    #     print('\n' + str(counter))
    #     print('Concert: ', title, '\nCountry: ', country, '\nState: ',
    #           state, '\nCity: ', city, '\nlongitude = ', longitude,
    #           '\nlatitude = ', latitude)
    #


if __name__ == '__main__':
    main()
