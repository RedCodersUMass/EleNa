import logging
import networkx as nx
import osmnx as ox
from collections import deque, defaultdict
from src.constants import constants
from heapq import *
from src.server.algorithms import Djikstra

MAXIMIZE = "max"
MINIMIZE = "min"
EMPTY = "empty"
ELEVATION_DROP = "elevation_drop"
ELEVATION_GAIN = "elevation_gain"


class ShortestRoute:

    def __init__(self, graph):
        self.logger = logging.getLogger(__name__)
        self.graph = graph
        self.best_path = [[], 0.0, float('-inf'), 0.0, EMPTY]
        self.starting_node = None
        self.ending_node = None
        self.shortest_route = None
        self.shortest_dist = None

    # Calculates shortest route between starting and ending node
    def get_shortest_route(self, starting_point, ending_point):
        graph = self.graph
        self.starting_node, self.ending_node = None, None

        self.starting_node = ox.get_nearest_node(graph, point=starting_point)
        self.ending_node = ox.get_nearest_node(graph, point=ending_point)

        # returns the shortest route from starting node to ending node based on distance
        self.shortest_route = nx.shortest_path(graph, source=self.starting_node, target=self.ending_node, weight='length')

        print("Calculated shortest route between source and destination")

        # ox.get_route function returns list of edge length for above shortest route
        self.shortest_dist = sum(ox.utils_graph.get_route_edge_attributes(graph, self.shortest_route, 'length'))

        shortest_route_lat_long = [[graph.nodes[route_node]['x'], graph.nodes[route_node]['y']] for route_node in
                                   self.shortest_route]
        
        return shortest_route_lat_long
