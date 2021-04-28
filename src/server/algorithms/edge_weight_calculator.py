from .constants import *

class EdgeWeightCalculator:
    @classmethod
    def get_weight(cls, G, node_1, node_2, weight_type=NORMAL):
        if weight_type == NORMAL:
            try :
                return G.edges[node_1, node_2 ,0][LENGTH]
            except :
                return G.edges[node_1, node_2][WEIGHT]
        elif weight_type == ELEVATION_DIFFERENCE or weight_type == BOTH:
            return G.nodes[node_2][ELEVATION] - G.nodes[node_1][ELEVATION]
        elif weight_type == ELEVATION_GAIN:
            return max(0.0, G.nodes[node_2][ELEVATION] - G.nodes[node_1][ELEVATION])
        elif weight_type == ELEVATION_DROP:
            return max(0.0, G.nodes[node_1][ELEVATION] - G.nodes[node_2][ELEVATION])
        else:
            return abs(G.nodes[node_1][ELEVATION] - G.nodes[node_2][ELEVATION])
