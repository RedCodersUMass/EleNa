import osmnx as ox
import networkx as nx
from collections import deque, defaultdict
from abc import ABC, abstractmethod
from .algorithms_interface import AlgorithmsInterface
from .constants import *
from .edge_weight_calculator import *


class AlgorithmsAbstract(AlgorithmsInterface):
    def __init__(self, G, shortest_dist, thresh = 0.0, elevation_mode = MAXIMIZE, start_node = None, end_node = None):

        self.G = G
        self.elevation_mode = elevation_mode
        self.thresh = thresh
        self.optimal_path = [[], 0.0, float('-inf'), float('-inf'), EMPTY]
        self.start_node= start_node
        self.end_node =end_node
        self.shortest_path_total_weight = shortest_dist
        if elevation_mode == MINIMIZE:
            self.optimal_path[2] = float('inf')

    def setGraph(self, G):
        self.G = G

    def get_path_weight(self, route, weight_attribute=BOTH, isPiecewise=False):
        # Compute total weight for a  complete given route
        total = 0
        if isPiecewise :
            piece_elevation = []

        for i in range(len(route)-1):
            diff = EdgeWeightCalculator.get_weight(self.G, route[i], route[i+1], weight_attribute)
            total += diff

            if isPiecewise:
                piece_elevation.append(diff)

        if isPiecewise:
            return total, piece_elevation
        else:
            return total

    def check_nodes(self):
        # Checks if start or end nodes are None values
        if self.start_node is None or self.end_node is None:
            return False
        return True

    @abstractmethod
    def shortest_path(self):
        pass
