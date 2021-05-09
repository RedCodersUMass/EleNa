import logging

import networkx as nx
import osmnx as ox

from src.constants.constants import *
from src.model.PathInformation import PathInformation
from src.model.utils import get_path_weight

MAXIMIZE = "max"
MINIMIZE = "min"
EMPTY = "empty"
ELEVATION_DROP = "elevation_drop"
ELEVATION_GAIN = "elevation_gain"


class ShortestRoute:
    """
    This class computes the shortest path without taking elevation into consideration.
    """

    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.graph = graph
        self.starting_node = None
        self.ending_node = None
        self.shortest_route = None
        self.shortest_dist = None

    def get_shortest_route(self, starting_point, ending_point):
        """
        This method computes shortest route by only taking edge weights into consideration.
        Args:
            starting_point: the (lat,lng) of the starting point
            ending_point: the (lat,lng) of the destination point

        Returns:
            RouteInformation object
        """
        graph = self.graph
        self.starting_node, self.ending_node = None, None

        self.starting_node, d1 = ox.get_nearest_node(graph, point=starting_point, return_dist=True)
        self.ending_node, d2 = ox.get_nearest_node(graph, point=ending_point, return_dist=True)

        # returns the shortest route from starting node to ending node based on distance
        self.shortest_route = nx.shortest_path(graph, source=self.starting_node, target=self.ending_node,
                                               weight='length')

        print("Calculated shortest route between source and destination")

        shortest_path_information = PathInformation()
        shortest_path_information.set_starting_node(self.starting_node)
        shortest_path_information.set_ending_node(self.ending_node)
        shortest_path_information.set_algorithm_name(SHORTEST)
        shortest_path_information.set_total_gain(get_path_weight(self.graph, self.shortest_route, ELEVATION_GAIN))
        shortest_path_information.set_total_drop(0)
        shortest_path_information.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                            for route_node in self.shortest_route])
        shortest_path_information.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(graph, self.shortest_route, 'length')))

        return shortest_path_information
