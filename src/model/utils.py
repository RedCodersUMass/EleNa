from geopy.geocoders import Nominatim
from src.constants.constants import *


def get_address_from_coordinates(coordinates):
    """
    This method fetches the address from the coordinates using Nominatim API.
    Args:
        coordinates: the latitude, longitude coordinates.

    Returns:
        address in human readable format.
    """
    return Nominatim(user_agent="myGeocoder").reverse(coordinates).address


def get_path_weight(graph, route, weight_attribute):
    """
    Gets path weights,

    Args:
        graph: graph
        route: route
        weight_attribute: weight_attribute

    Returns:
        total: total weight
    """
    total = 0
    for i in range(len(route) - 1):
        total += get_weight(graph, route[i], route[i + 1], weight_attribute)
    return total


def get_weight(graph, node_1, node_2, weight_type=NORMAL):
    """
    This method computes the weight of the edge based on elevation difference or the path length.
    Args:
        graph: The input osmnx graph object
        node_1: the starting node
        node_2: the ending node
        weight_type: either normal/elevation

    Returns:
        the weight of the edge between the input nodes
    """
    if weight_type == NORMAL:
        try:
            return graph.edges[node_1, node_2, 0][LENGTH]
        except:
            return graph.edges[node_1, node_2][WEIGHT]
    elif weight_type == ELEVATION_GAIN:
        return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])
