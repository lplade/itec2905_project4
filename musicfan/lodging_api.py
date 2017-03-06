from googleplaces import GooglePlaces, types, lang

from secrets import *

google_places = GooglePlaces(GOOGLE_PLACES_API_WEB_SERVICE_KEY)


def get_query_lodging(city, state=None, country=None, venue=None, radius=3200,
                      cheap_limit=4):
    """
    Sends a lodging search request to Google Places API Web Service
    :param country:
    :param state:
    :param city:
    :param cheap_limit: max price on a scale of 1 to 4
    :param venue: building where event is happening
    :param radius: defaults to 2 mile radius
    :return:
    """
    # build a string for location query
    # TODO pass in lat/long instead?
    loc_string = ""
    if venue:
        loc_string += "{}, ".format(venue)
    loc_string += "{}, ".format(city)
    if state:
        loc_string += "{}, ".format(state)
    if country:
        loc_string += "{}".format(country)

    query_result = google_places.nearby_search(
        # TODO figure out how to pass maxprice
        # Or maybe just filter result
        location=loc_string,
        radius=radius,
        type=types.TYPE_LODGING
    )

    return query_result


def main():
    """
    test stub
    :return:
    """
    city = input("City to search for? ")

    rs = get_query_lodging(city)

    for place in rs.places:

        # We have to do this to get the details
        place.get_details()

        print("{} {} Rating: {} Address: {} Phone: {}".format(
            place.name, place.place_id, place.rating, place.formatted_address,
            place.local_phone_number
        ))


if __name__ == "__main__":
    main()
