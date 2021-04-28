from abc import ABC, abstractmethod
from collections import deque, defaultdict
import networkx as nx
import osmnx as ox
from src.model.algorithms.edge_weight_calculator import EdgeWeightCalculator
from src.model.algorithms.algorithms_interface import AlgorithmsInterface
from src.constants.constants import *


class AlgorithmsAbstract(AlgorithmsInterface):
    def __init__(self, graph, shortest_distance, path_limit=0.0, elevation_strategy=MAXIMIZE, starting_node=None,
                 ending_node=None):

        self.graph = graph
        self.elevation_strategy = elevation_strategy
        self.path_limit = path_limit
        self.optimal_route = [[], 0.0, float('-inf'), float('-inf'), EMPTY]
        self.starting_node = starting_node
        self.ending_node = ending_node
        self.shortest_route_total_weight = shortest_distance
        if elevation_strategy == MINIMIZE:
            self.optimal_route[2] = float('inf')

    def set_graph(self, graph):
        self.graph = graph

    def get_path_weight(self, route, weight_attribute=BOTH, isPiecewise=False):
        # Compute total weight for a  complete given route
        total = 0
        if isPiecewise:
            piece_elevation = []

        for i in range(len(route) - 1):
            diff = EdgeWeightCalculator.get_weight(self.graph, route[i], route[i + 1], weight_attribute)
            total += diff

            if isPiecewise:
                piece_elevation.append(diff)

        if isPiecewise:
            return total, piece_elevation
        else:
            return total

    def check_valid_starting_ending_nodes(self):
        # Checks if starting or ending nodes have None values
        if self.starting_node is None or self.ending_node is None:
            return False
        return True

    @abstractmethod
    def shortest_route(self):
        pass
