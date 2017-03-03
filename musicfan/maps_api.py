# Things that interact with Google Maps API
from secrets import *
import geocoder
import json


def find_location_coordinates(location_string):
    """
    Looks up coordinates for a location
    :param location_string: Location. Ideally, City, State
    :return: latitude, longitude
    """
    g = geocoder.google(location=location_string, key=GOOGLE_MAPS_API_KEY)
    results = g.json
    parsed_json = json.loads(results)

    latitude = float(parsed_json['lat'])
    longitude = float(parsed_json['lng'])

    return latitude, longitude

