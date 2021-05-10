from geopy.geocoders import Nominatim
from src.constants.constants import *
import networkx as nx
from src.constants.constants import *
from heapq import heappush, heappop
from itertools import count
from networkx.algorithms.shortest_paths.weighted import _weight_function


def astar_algorithm(G, source, target, heuristic, weight):
    """
    This method returns a list of nodes in a shortest path between source and target using astar algorithm.
    Dijkstra algorithm can set heuristic value as 0 to compute the shortest route.
    The implementation has been inspired by networkx blogs.

    Args:
        G : NetworkX graph
        source : Starting node for path
        target : Ending node for path
        heuristic : A function to evaluate the estimate of the distance from the a node to the target.
        weight : accepts a string or function to get the edge weights

    Returns: a list of nodes in a shortest path between source and target.

    """
    if source not in G or target not in G:
        print("Either source or target is not in the graph")

    if heuristic is None:
        def heuristic(u, v):
            return 0
    push, pop = heappush, heappop
    weight = _weight_function(G, weight)
    c = count()
    queue = [(0, next(c), source, 0, None)]
    enqueued, explored = {}, {}
    while queue:
        _, __, curnode, dist, parent = pop(queue)
        if curnode == target:
            path = [curnode]
            node = parent
            while node is not None:
                path.append(node)
                node = explored[node]
            path.reverse()
            return path
        if curnode in explored:
            if explored[curnode] is None:
                continue
            qcost, h = enqueued[curnode]
            if qcost < dist:
                continue
        explored[curnode] = parent
        for neighbor, w in G[curnode].items():
            ncost = dist + weight(curnode, neighbor, w)
            if neighbor in enqueued:
                qcost, h = enqueued[neighbor]
                if qcost <= ncost:
                    continue
            else:
                h = heuristic(neighbor, target)
            enqueued[neighbor] = ncost, h
            push(queue, (ncost + h, next(c), neighbor, ncost, curnode))
    raise nx.NetworkXNoPath(f"Node {target} not reachable from {source}")


def get_address_from_coordinates(coordinates):
    """
    This method fetches the address from the coordinates using Nominatim API.
    Args:
        coordinates: the latitude, longitude coordinates.

    Returns:
        address in human readable format.
    """
    return Nominatim(user_agent="myGeocoder").reverse(coordinates).address


def get_path_weight(graph, route, weight_attribute):
    """
    Gets path weights,

    Args:
        graph: graph
        route: route
        weight_attribute: weight_attribute

    Returns:
        total: total weight
    """
    total = 0
    for i in range(len(route) - 1):
        total += get_weight(graph, route[i], route[i + 1], weight_attribute)
    return total


def get_weight(graph, node_1, node_2, weight_type=NORMAL):
    """
    This method computes the weight of the edge based on elevation difference or the path length.
    Args:
        graph: The input osmnx graph object
        node_1: the starting node
        node_2: the ending node
        weight_type: either normal/elevation

    Returns:
        the weight of the edge between the input nodes
    """
    if weight_type == NORMAL:
        try:
            return graph.edges[node_1, node_2, 0][LENGTH]
        except:
            return graph.edges[node_1, node_2][WEIGHT]
    elif weight_type == ELEVATION_GAIN:
        return max(0.0, graph.nodes[node_2][ELEVATION] - graph.nodes[node_1][ELEVATION])
