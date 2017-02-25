

# import urllib.parse
import requests
import json

class URLrequest():

    # The 'category' argument, also called 'c', is used to search within a category. TODO Enter key
    main_API = 'http://api.eventful.com/json/events/search?q=metallica&app_key=xxxxxxx'

    # Get the data in a json format
    json_data = requests.get(main_API).json()


    # This is to keep track  of the number of concerts.
    counter = 0

    print('\n**Here is the list of concerts for "name"**')
    # First loop, gets the first keys, thent it gets passed to the next one.
    for key, value in json_data['events'].items():
        # This loop has to be iter because is a list.

        for newValue in iter(value):
            counter += 1 # This is to count how many concerts are.
            # The counter has to be in this loop.

            # This loops each key and gets the value that it is needed
            for key in newValue:
                title = str(newValue['title'])
                state = str(newValue['region_name'])
                city = str(newValue['city_name'])
                country = str(newValue['country_name'])
                longitude = str(newValue['longitude'])
                latitude = str(newValue['latitude'])
                # TODO url? I didn't think that the url is necesary because we need
                # the one for the hotels and travel options only.

            # Print staments
            print('\n' + str(counter))
            print('Concert: ', title, '\nCountry: ', country, '\nState: ',\
                state, '\nCity: ', city, '\nlongitude = ', longitude,\
                 '\nlatitude = ', latitude)
        counter += 1


    # TODO get the elements and store them in a data base
    # TODO connet to Flask

def main():
    URLrequest()

if __name__ == '__main__':
    main()
