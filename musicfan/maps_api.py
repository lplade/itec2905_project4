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

    latitude = float(results['lat'])
    longitude = float(results['lng'])

    return latitude, longitude

