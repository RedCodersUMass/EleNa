from src.constants.constants import *


def update_route_json(coordinates):
    """
    This method converts coordinates to route_json response format
    Args:
        coordinates:

    Returns:
        route_json
    """
    route_json = {PROPERTIES: {}, GEOMETRY: {}, TYPE: FEATURE}
    route_json[GEOMETRY][TYPE] = LINESTRING
    route_json[GEOMETRY][COORDINATES] = coordinates
    return route_json
