import math
import logging
import networkx as nx
import osmnx as ox
from src.model.PathInformation import PathInformation
from src.model.utils import get_path_weight, astar_algorithm
from src.constants.constants import *
from heapq import heappush, heappop
from itertools import count

MAXIMIZE = "max"
MINIMIZE = "min"
EMPTY = "empty"
ELEVATION_DROP = "elevation_drop"
ELEVATION_GAIN = "elevation_gain"


class AstarRoute:
    """
    This class computes the shortest route considering elevation into account and uses Dijkstra algorithm.
    """

    def __init__(self, graph, shortest_dist, path_limit, elevation_strategy, starting_node, ending_node,
                 shortest_path_elevation_gain):
        self.logger = logging.getLogger(__name__)
        self.graph = graph
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.elevation_route = None
        self.shortest_dist = shortest_dist
        self.path_limit = path_limit
        self.elevation_strategy = elevation_strategy
        self.scaling_factor = 100
        self.elevation_distance = None
        self.shortest_path_elevation_gain = shortest_path_elevation_gain

    def dist(self, a, b):
        return self.graph.nodes[a]['dist_from_dest'] * 1 / self.scaling_factor

    def get_shortest_route(self):
        """
        This method computes shortest route by taking edge weights and elevation into consideration.

        Returns:
            RouteInformation object
        """
        graph = self.graph
        if self.elevation_strategy == MINIMIZE:
            min_max_factor = 1
        else:
            min_max_factor = -1
        self.elevation_route = nx.shortest_path(graph, source=self.starting_node, target=self.ending_node,
                                                weight='length')
        while self.scaling_factor < 10000:
            # returns the shortest route from starting node to ending node based on distance
            elevation_route = astar_algorithm(graph,
                                              source=self.starting_node,
                                              target=self.ending_node,
                                              heuristic=self.dist,
                                              weight=lambda u, v, d:
                                              math.exp(min_max_factor * d[0]['length'] * (
                                                          d[0]['grade'] + d[0]['grade_abs']) / 2)
                                              + math.exp((1 / self.scaling_factor) * d[0]['length']))
            elevation_distance = sum(ox.utils_graph.get_route_edge_attributes(graph, elevation_route, 'length'))
            elevation_gain = get_path_weight(self.graph, elevation_route, ELEVATION_GAIN)
            if elevation_distance <= (1 + self.path_limit) * self.shortest_dist and \
                    min_max_factor * elevation_gain <= min_max_factor * self.shortest_path_elevation_gain:
                self.elevation_route = elevation_route
                self.shortest_path_elevation_gain = elevation_gain
            self.scaling_factor *= 5

        shortest_path_information = PathInformation()
        shortest_path_information.set_algorithm_name(A_STAR)
        shortest_path_information.set_total_gain(get_path_weight(self.graph, self.elevation_route, ELEVATION_GAIN))
        shortest_path_information.set_total_drop(0)
        shortest_path_information.set_path([[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']]
                                            for route_node in self.elevation_route])
        shortest_path_information.set_distance(
            sum(ox.utils_graph.get_route_edge_attributes(graph, self.elevation_route, 'length')))

        return shortest_path_information
