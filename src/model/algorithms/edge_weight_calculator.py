from src.constants.constants import *


class EdgeWeightCalculator:
    @classmethod
    def get_weight(cls, graph, node_1, node_2, weight_type=NORMAL):
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
