import osmnx as ox
import networkx as nx
from heapq import *
from collections import deque, defaultdict
from .algorithms_abstract import AlgorithmsAbstract
from .constants import *
from .edge_weight_calculator import *

DJIKSTRA_SCALING_FACTOR = 0.25


class Djikstra(AlgorithmsAbstract):
    def __init__(self, G, shortest_dist, thresh=0.0, elevation_mode=MAXIMIZE, start_node=None, end_node=None):
        super(Djikstra, self).__init__(G, shortest_dist, thresh, elevation_mode, start_node, end_node)

    def get_route(self, parent_node, dest):
        # "returns the path given a parent mapping and the final dest"
        path = [dest]
        curr = parent_node[dest]
        while curr != -1:
            path.append(curr)
            curr = parent_node[curr]
        return path[::-1]

    def shortest_path(self):

        if not self.check_nodes():
            return

        G, thresh, shortest_path_weight, elevation_mode = self.G, self.thresh, self.shortest_path_total_weight, self.elevation_mode
        start_node, end_node = self.start_node, self.end_node

        min_heap = [(0.0, 0.0, start_node)]

        visited = set()
        score_info = {start_node: 0}

        # Set parent node dictionary
        parent_node = defaultdict(int)
        parent_node[start_node] = -1

        while min_heap:

            this_score, this_distance, this_node = heappop(min_heap)

            if this_node not in visited:
                visited.add(this_node)

                # Break if end node is reached
                if this_node == end_node:
                    break

                for adj in G.neighbors(this_node):
                    if adj in visited:
                        continue

                    prev = score_info.get(adj, None)  # get past priority of the node
                    edge_weight = EdgeWeightCalculator.get_weight(self.G, this_node, adj, NORMAL)

                    # Update distance btw the nodes depending on maximize(subtract) or minimize elevation(add)
                    updated_score = self.get_updated_score(this_node, adj, edge_weight, this_score)

                    updated_distance = this_distance + edge_weight

                    if updated_distance <= shortest_path_weight * (1.0 + thresh) and (
                            prev is None or updated_score < prev):
                        parent_node[adj] = this_node
                        score_info[adj] = updated_score
                        heappush(min_heap, (updated_score, updated_distance, adj))

        if not this_distance:
            return

        route = self.get_route(parent_node, end_node)
        gain = self.get_path_weight(route, ELEVATION_GAIN)
        drop = self.get_path_weight(route, ELEVATION_DROP)

        return [route[:], this_distance, gain, drop, DJIKSTRA]

    def get_updated_score(self, node_1, node_2, edge_weight, this_score):

        # Calculates updated priority of an edge using the edge length (Scaled by the scaling factor)

        elevation_mode = self.elevation_mode
        thresh = self.thresh
        scaled_edge_length = edge_weight * DJIKSTRA_SCALING_FACTOR

        if elevation_mode == MAXIMIZE:
            return scaled_edge_length + EdgeWeightCalculator.get_weight(self.G, node_1, node_2,
                                                                        ELEVATION_DROP) + this_score
        else:
            return scaled_edge_length + EdgeWeightCalculator.get_weight(self.G, node_1, node_2,
                                                                        ELEVATION_GAIN) + this_score
