import osmnx as ox
import networkx as nx
from heapq import *
from collections import deque, defaultdict
from .algorithms_abstract import AlgorithmsAbstract
from src.constants.constants import *
from .edge_weight_calculator import *
from ..PathInformation import PathInformation

A_STAR_SCALING_ELEMENT = 0.1


class AStarAlg(AlgorithmsAbstract):
    def __init__(self, graph, shortest_distance, path_limit=0.0, elevation_strategy=MAXIMIZE, starting_node=None,
                 ending_node=None):
        super(AStarAlg, self).__init__(graph, shortest_distance, path_limit, elevation_strategy, starting_node,
                                       ending_node)

    def path_rebuild(self, parent_node_mapping, current_node):  # Rebuilds the path

        if parent_node_mapping is None or current_node is None:
            return
        path = [current_node]

        while current_node in parent_node_mapping:
            current_node = parent_node_mapping[current_node]
            path.append(current_node)

        return path

    def get_edge_weight(self, current_node, next_node):
        elevation_strategy = self.elevation_strategy
        if elevation_strategy == MINIMIZE:
            return EdgeWeightCalculator.get_weight(self.graph, current_node, next_node, ELEVATION_GAIN)
        elif elevation_strategy == MAXIMIZE:
            return EdgeWeightCalculator.get_weight(self.graph, current_node, next_node, ELEVATION_DROP)

    def heuristic(self, n):
        return self.graph.nodes[n][DESTINATION_DISTANCE] * A_STAR_SCALING_ELEMENT

    def shortest_route(self):

        visited_nodes = set()  # contains the data of nodes visited
        unvisited_nodes = set()  # contains the data of nodes not visited

        parent_node_mapping, route_score, other_route_score, total_score = {}, {}, {}, {}  # Stores parent node information

        if not self.check_valid_starting_ending_nodes():
            return

        graph, shortest_route_total_weight, path_limit, elevation_strategy = self.graph, self.shortest_route_total_weight, self.path_limit, self.elevation_strategy
        starting_node = self.starting_node
        ending_node = self.ending_node

        # Marking the starting node unvisited
        unvisited_nodes.add(starting_node)
        # Initializing g scores values for nodes
        for node in graph.nodes():
            route_score[node] = float("inf")
            other_route_score[node] = float("inf")

        route_score[starting_node] = other_route_score[starting_node] = 0

        total_score[starting_node] = graph.nodes[starting_node][DESTINATION_DISTANCE] * 0.1

        while len(unvisited_nodes):

            current_node = min([(node, total_score[node]) for node in unvisited_nodes], key=lambda t: t[1])[0]

            if current_node == ending_node:
                route = self.path_rebuild(parent_node_mapping, current_node)
                current_distance = self.get_path_weight(route, NORMAL)
                path_information = PathInformation()
                path_information.set_algorithm_name(A_STAR)
                path_information.set_total_gain(self.get_path_weight(route, ELEVATION_GAIN))
                path_information.set_total_drop(self.get_path_weight(route, ELEVATION_DROP))
                path_information.set_path(route)
                path_information.set_distance(current_distance)

                return path_information

            # Adding the current node to visited list, removing current node from unvisited list
            unvisited_nodes.remove(current_node)
            visited_nodes.add(current_node)

            # Loop over adjacent nodes and update g and f scores
            self.update_g_and_f_scores(graph, parent_node_mapping, route_score, shortest_route_total_weight, current_node,
                                    path_limit,
                                    total_score,
                                    unvisited_nodes, visited_nodes, other_route_score)

            return PathInformation()

    def update_g_and_f_scores(self, G, parent_node_mapping, route_score, shortest_route_total_weight, current_node,
                           path_limit, total_score,
                           unvisited_nodes, visited_nodes, other_route_score):
        for adjacent_node in G.neighbors(current_node):

            if adjacent_node in visited_nodes:
                continue

            g_route_score = route_score[current_node] + self.get_edge_weight(current_node, adjacent_node)
            f_route_score = other_route_score[current_node] + EdgeWeightCalculator.get_weight(self.graph, current_node,
                                                                                              adjacent_node,
                                                                                              NORMAL)

            if f_route_score <= (1 + path_limit) * shortest_route_total_weight and adjacent_node not in unvisited_nodes:
                unvisited_nodes.add(adjacent_node)
            else:
                if (
                        f_route_score >= (1 + path_limit) * shortest_route_total_weight) or (
                        g_route_score >= route_score[adjacent_node]):
                    continue

            parent_node_mapping[adjacent_node] = current_node
            route_score[adjacent_node] = g_route_score
            other_route_score[adjacent_node] = f_route_score
            total_score[adjacent_node] = route_score[adjacent_node] + self.heuristic(adjacent_node)
