import urllib.request
import urllib.parse
import requests

# This includes our secret API key
from secrets import *

from mapdistance import distance


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
        self.distance = None

    def set_distance_from_origin(self, origin_longitude, origin_latitude):
        """
        Sets the distance to this Concert from the origin
        :param origin_longitude:
        :param origin_latitude:
        :return:
        """
        self.distance = \
            self.find_distance_from_origin(origin_longitude, origin_latitude)
        return True

    def find_distance_from_origin(self, origin_longitude, origin_latitude):
        """
        Standalone function to find distance from origin
        :param origin_longitude:
        :param origin_latitude:
        :return:
        """
        return distance(origin_latitude, origin_longitude,
                        self.latitude, self.longitude)


def search_by_band(band_name):
    """

    :param band_name: name of artist we are searching for
    :return: list of Concert
    """

    # distance filter is handled by main app now

    # We have to use .urlencode to properly encode spaces and such into ASCII
    # URL string
    params = urllib.parse.urlencode(({
        'q': band_name,
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
            event_object = Concert(event_id=str(newValue['id']),
                                   title=str(newValue['title']),
                                   date=str(newValue['start_time']),
                                   region_name=str(newValue['region_name']),
                                   city_name=str(newValue['city_name']),
                                   country_name=str(newValue['country_name']),
                                   longitude=float(newValue['latitude']),
                                   latitude=float(newValue['latitude']),
                                   venue_name=str(newValue['venue_name']),
                                   venue_address=str(newValue['venue_address'])
                                   )

            event_list.append(event_object)

    return event_list


def main():
    band = input("What band to search for? ")

    # concert_list = search_by_band(band)
    search_by_band(band)

    # TODO simple interactive console test routine should go here

if __name__ == '__main__':
    main()
