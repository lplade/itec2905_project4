# this is just a placeholer for the flight search API module
import requests
import json
from skyscanner_resources.skyscanner_endpoints import SkyScannerEndpoints


class FlightCachePrices:

    def __init__(self):
        self.originPlace = None
        self.destinationPlace = None
        # The outbound date. Format “yyyy-mm-dd”, “yyyy-mm” or “anytime”.
        self.outboundPartialDate = None
        # The return date. Format “yyyy-mm-dd”, “yyyy-mm” or “anytime”. Use empty string for oneway trip.
        self.inboundPartialDate = None
        self.headers = {'Accept': 'application/json'}
        self.responseData = None
        self.resourceFolder = 'skyscanner_resources/'
        # all supported locations
        self.geoResourcesFileName = 'geo.json'
        # all supported north american locations
        self.geoNorthAmericaResourcesFileName = 'geo_north_america.json'

    def load_global_locations(self):

        # try to load local data
        try:
            with open(self.resourceFolder + self.geoResourcesFileName, 'r') as all_geo:

                data = json.load(all_geo)

                return data

        except FileNotFoundError as e:
            # get remote data
            print('local data not found, error with loading all geo data from file', e)

            geo_url = SkyScannerEndpoints().get_all_geo()

            response = self.get_request(geo_url)

            all_geo_json = response.json()

            FlightUtils.write_to_file(self.resourceFolder + self.geoResourcesFileName, all_geo_json)

    def get_request(self, url):
        r = requests.get(url, self.headers)
        return r

    def load_north_america_locations(self):
        try:
            # see if we have local data for supported global locations
            # if not load it with a GET call
            data = self.load_global_locations()

            # load north america region from global geo.json
            for continent in data['Continents']:
                if continent['Id'] == 'N':
                    for country in continent['Countries']:
                        if country['Id'] == 'US':
                            FlightUtils.write_to_file(
                                self.resourceFolder + self.geoNorthAmericaResourcesFileName, country
                            )

        except Exception as e:
            print('Error opening file in skyscanner_resources/', e)

    def get_data(self):
        if self.responseData is None:
            return 'No response data set'
        return self.responseData

    def __str__(self):
        return


class FlightUtils:
    @staticmethod
    def write_to_file(file_path, data_json,):
        try:
            with open(file_path, 'w') as fp:
                json.dump(data_json, fp)
        except Exception as e:
            print('Error writing to file', e)

f = FlightCachePrices()
f.load_north_america_locations()
