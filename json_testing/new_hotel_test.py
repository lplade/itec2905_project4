# This is a test to see if there is an advantage to writing a Google Places
# query from scratch instead of using the pip module
# Unfortunately, Google Places still does not return
# values for hotel prices
# Specifying a "max_price" for this returns an empty data set. :(

import urllib.request
import urllib.parse
import requests
import json  # useful for debugging
import logging

from musicfan.secrets import *


def geocode_location(location):

    params = urllib.parse.urlencode({
        'address': location,
        'key': GOOGLE_MAPS_API_KEY,
    })

    api_url = \
        'https://maps.googleapis.com/maps/api/geocode/json?%s' \
        % params

    json_data = requests.get(api_url).json()
    if json_data['status'] == "OK":
        geo_coord = json_data['results'][0]['geometry']['location']
    else:
        logging.warning("Response status \"{}\", no coordinates set".format(json_data['status']))
        geo_coord = None

    return geo_coord


def search_by_location(location, radius=3200, cheap_level=4):

    geo_coords = geocode_location(location)

    params = urllib.parse.urlencode({
        'key': GOOGLE_PLACES_API_WEB_SERVICE_KEY,
        'location': str(geo_coords['lat']) + ',' + str(geo_coords['lng']),
        'radius': radius,
        'type': 'lodging'
    })
    api_url = \
        'https://maps.googleapis.com/maps/api/place/nearbysearch/json?%s' \
        % params

    json_data = requests.get(api_url).json()

    return json_data


def main():
    query = input("What place to search around? ")

    json_data = search_by_location(query)

    print(json.dumps(json_data, indent=4))

if __name__ == '__main__':
    main()
