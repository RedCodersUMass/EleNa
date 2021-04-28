import osmnx as ox
from src.model.GraphGenerator import GraphGenerator
from src.model.ShortestRoute import ShortestRoute
from src.model.algorithms.dijkstra_alg import *
from src.model.algorithms.algorithms_abstract import *
from src.model.utils import *
from src.view.view import *
from src.constants.constants import *


class Model:
    def __init__(self):
        self.mapbox_api_key = None
        self.shortest_path_algorithm = None
        self.graph = None
        self.shortest_route_object = None
        self.observer = None
        self.algorithm = None
        self.algorithm_object = None

    def register_observer(self, observer):
        self.observer = observer

    def set_algorithm(self, algorithm):
        self.algorithm = algorithm

    def get_mapbox_api(self):
        return self.mapbox_api_key

    def set_mapbox_api(self, api_key):
        self.mapbox_api_key = api_key

    def get_shortest_path_algorithm(self):
        return self.shortest_path_algorithm

    def set_shortest_path_algorithm(self, algorithm):
        self.shortest_path_algorithm = algorithm

    def set_shortest_route_object(self, coord_end):
        self.graph = GraphGenerator().generate_elevation_graph(coord_end)
        self.shortest_route_object = ShortestRoute(self.graph)

    def get_best_route_object(self):
        self.graph = GraphGenerator().generate_elevation_graph(coord_end)
        self.shortest_route_object = ShortestRoute(self.graph)

    def set_algorithm_object(self, starting_node, ending_node, shortest_dist, path_limit, elevation_strategy):
        if self.algorithm == DIJKSTRA:
            self.algorithm_object = Djikstra_Alg(self.graph, shortest_dist, path_limit, elevation_strategy,
                                                 starting_node, ending_node)

    def print_route_information(self, route):
        print("------------------------------------------------")
        print("Algorithm Strategy:" + route[4])
        print("Total Distance: " + str(route[1]))
        print("Elevation Gain: " + str(route[2]))
        print("Elevation Drop: " + str(route[3]))

    def generate_paths(self, origin, destination, path_limit, elevation_strategy):
        # calculate shortest path
        self.set_shortest_route_object(destination)

        starting_node, ending_node, shortest_route, shortest_route_lat_long, shortest_dist = \
            self.shortest_route_object.get_shortest_route(origin, destination)

        path_limit = path_limit / 100.0
        self.set_algorithm_object(starting_node, ending_node, shortest_dist, path_limit, elevation_strategy)

        shortest_path_information = [shortest_route_lat_long, shortest_dist,
                                     self.algorithm_object.get_path_weight(shortest_route, ELEVATION_GAIN),
                                     self.algorithm_object.get_path_weight(shortest_route, ELEVATION_DROP),
                                     SHORTEST]
        self.print_route_information(shortest_path_information)

        if path_limit == 0:
            return shortest_path_information, shortest_path_information

        elevation_route = self.algorithm_object.shortest_route()

        self.print_route_information(elevation_route)

        # If elevation route doesn't return a shortest path based on elevation requirements
        if (elevation_strategy == MAXIMIZE and elevation_route[2] == float('-inf')) or (
                elevation_strategy == MINIMIZE and elevation_route[3] == float('-inf')):
            elevation_route = [[], 0.0, 0, 0, EMPTY]

        elevation_route[0] = [[self.graph.nodes[route_node]['x'], self.graph.nodes[route_node]['y']] for route_node in
                              elevation_route[0]]

        # If the elevation route does not match the elevation requirements
        # if ((elevation_strategy == MAXIMIZE and elevation_route[2] < shortest_path_information[2]) or (
        #        elevation_strategy == MINIMIZE and elevation_route[2] > shortest_path_information[2])):
        #    elevation_route = shortest_path_information

        self.observer.update_notifier(shortest_path_information, elevation_route, get_address_from_coordinates(origin),
                                      get_address_from_coordinates(destination))
