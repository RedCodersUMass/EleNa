from geopy.geocoders import Nominatim


def get_address_from_coordinates(coordinates):
    return Nominatim(user_agent="chrome").reverse(coordinates).address
