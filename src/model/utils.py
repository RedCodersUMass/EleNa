from geopy.geocoders import Nominatim
from src.constants.constants import *


def get_address_from_coordinates(coordinates):
    return Nominatim(user_agent="myGeocoder").reverse(coordinates).address


def get_path_weight(graph, route, weight_attribute, is_piecewise=False):
    # Compute total weight for a  complete given route
    total = 0
    if is_piecewise:
        piece_elevation = []

    for i in range(len(route) - 1):
        diff = get_weight(graph, route[i], route[i + 1], weight_attribute)
        total += diff

        if is_piecewise:
            piece_elevation.append(diff)

    if is_piecewise:
        return total, piece_elevation
    else:
        return total


def get_weight(graph, node_1, node_2, weight_type=NORMAL):
    if weight_type == NORMAL:
        try:
            return graph.edges[node_1, node_2, 0][LENGTH]
        except:
            return graph.edges[node_1, node_2][WEIGHT]
    elif weight_type == ELEVATION_GAIN:
        return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])
    elif weight_type == ELEVATION_DROP:
        return max(0.0, graph.nodes[node_1][ELEVATION] - graph.nodes[node_2][ELEVATION])
    else:
        return abs(graph.nodes[node_1][ELEVATION] - graph.nodes[node_2][ELEVATION])
