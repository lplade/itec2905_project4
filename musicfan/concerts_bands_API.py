import urllib.request
import urllib.parse
import requests
# import json

# This includes our secret API key
from secrets import *


class Concert:
    # Note that the band name is not stored here

    def __init__(self, event_id, title, date, region_name, city_name,
                 country_name, longitude, latitude, venue_name, venue_address):
        self.event_id = event_id
        self.title = title
        self.date = date  # what format is this stored in?
        self.region_name = region_name  # State, in USA
        self.city_name = city_name
        self.country_name = country_name
        self.longitude = longitude
        self.latitude = latitude
        self.venue_name = venue_name
        self.venue_address = venue_address


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
                event_id = str(newValue['id'])
                title = str(newValue['title'])
                state = str(newValue['region_name'])
                city = str(newValue['city_name'])
                country = str(newValue['country_name'])
                longitude = float(newValue['longitude'])
                latitude = float(newValue['latitude'])
                venue_name = str(newValue['venue_name'])
                venue_address = str(newValue['venue_address'])
                date = str(newValue['start_time'])
                # TODO url? I didn't think that the url is necessary because we need
                # the one for the hotels and travel options only.
                    # I agree, Boris

                event_object = Concert(event_id=event_id,
                                       title=title,
                                       date=date,
                                       region_name=state,
                                       city_name=city,
                                       country_name=country,
                                       longitude=longitude,
                                       latitude=latitude,
                                       venue_name=venue_name,
                                       venue_address=venue_address)

                event_list.append(event_object)

            # # This is to keep track  of the number of concerts.
            # # TODO This block is to check the api function, uncomment to see it running.
            # for concert in event_list:
            #     # Print staments
            #     print('\nId: ', event_id,'\nConcert: ', title, '\nCountry: ', country, '\nState: ',
            #           state, '\nCity: ', city, '\nlongitude = ', longitude,
            #           '\nlatitude = ', latitude, '\ndate = ', date, '\nvenue_name = ', venue_name)

    return event_list


def main():
    band = input("What band to search for? ")

    # concert_list = search_by_band(band)
    search_by_band(band)

    # TODO simple interactive console test routine should go here

if __name__ == '__main__':
    main()
