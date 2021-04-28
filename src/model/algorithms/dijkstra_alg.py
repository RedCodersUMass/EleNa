import osmnx as ox
import networkx as nx
from heapq import *
from collections import deque, defaultdict
from src.model.algorithms.algorithms_abstract import AlgorithmsAbstract
from constants import *
from src.model.algorithms.algorithms_abstract import EdgeWeightCalculator
from src.constants.constants import *


class Djikstra_Alg(AlgorithmsAbstract):
    def __init__(self, graph, shortest_distance, path_limit=0.0, elevation_strategy=MAXIMIZE, starting_node=None,
                 ending_node=None):
        super(Djikstra_Alg, self).__init__(graph, shortest_distance, path_limit, elevation_strategy, starting_node,
                                       ending_node)

    def get_route(self, parent_node, destination):
        # "returns the path given a parent mapping and the final destination"
        path = [destination]
        curr = parent_node[destination]
        while curr != -1:
            path.append(curr)
            curr = parent_node[curr]
        return path[::-1]

    def shortest_route(self):

        if not self.check_valid_starting_ending_nodes():
            return

        graph, path_limit, shortest_route_weight, elevation_strategy = self.graph, self.path_limit,\
                                                                       self.shortest_route_total_weight,\
                                                                       self.elevation_strategy
        starting_node, ending_node = self.starting_node, self.ending_node

        min_heap = [(0.0, 0.0, starting_node)]

        visited_nodes = set()
        score_info = {starting_node: 0}

        # Set parent node dictionary
        parent_node = defaultdict(int)
        parent_node[starting_node] = -1

        while min_heap:

            this_score, this_distance, this_node = heappop(min_heap)

            if this_node not in visited_nodes:
                visited_nodes.add(this_node)

                # Break if end node is reached
                if this_node == ending_node:
                    break

                for adjacent_node in graph.neighbors(this_node):
                    if adjacent_node in visited_nodes:
                        continue

                    prev = score_info.get(adjacent_node, None)  # get past priority of the node
                    edge_weight = EdgeWeightCalculator.get_weight(self.graph, this_node, adjacent_node, NORMAL)

                    # Update distance btw the nodes depending on maximize(subtract) or minimize elevation(add)
                    updated_score = self.get_updated_score(this_node, adjacent_node, edge_weight, this_score)

                    updated_distance = this_distance + edge_weight

                    if updated_distance <= shortest_route_weight * (1.0 + path_limit) and (
                            prev is None or updated_score < prev):
                        parent_node[adjacent_node] = this_node
                        score_info[adjacent_node] = updated_score
                        heappush(min_heap, (updated_score, updated_distance, adjacent_node))

        if not this_distance:
            return

        route = self.get_route(parent_node, ending_node)
        gain = self.get_path_weight(route, ELEVATION_GAIN)
        drop = self.get_path_weight(route, ELEVATION_DROP)

        return [route[:], this_distance, gain, drop, DIJKSTRA]

    def get_updated_score(self, node_1, node_2, edge_weight, this_score):

        # Calculates updated priority of an edge using the edge length (Scaled by the scaling factor)

        elevation_strategy = self.elevation_strategy
        scaled_edge_length = edge_weight * DJIKSTRA_SCALING_FACTOR

        if elevation_strategy == MAXIMIZE:
            return scaled_edge_length + EdgeWeightCalculator.get_weight(self.graph, node_1, node_2,
                                                                        ELEVATION_DROP) + this_score
        else:
            return scaled_edge_length + EdgeWeightCalculator.get_weight(self.graph, node_1, node_2,
                                                                        ELEVATION_GAIN) + this_score
