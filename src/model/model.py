from src.model.GraphGenerator import GraphGenerator
from src.model.ShortestRoute import ShortestRoute
from src.model.utils import get_address_from_coordinates
from src.view.view import *
from src.constants.constants import *
from src.model.PathInformation import PathInformation


class Model:
    def __init__(self):
        self.mapbox_api_key = None
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

    def set_shortest_route_object(self, coord_end):
        self.graph = GraphGenerator().generate_elevation_graph(coord_end)
        self.shortest_route_object = ShortestRoute(self.graph)

    def set_algorithm_object(self, starting_node, ending_node, shortest_dist, path_limit, elevation_strategy):
        self.algorithm_object = self.algorithm(self.graph, shortest_dist, path_limit, elevation_strategy,
                                               starting_node, ending_node)

    def print_route_information(self, route):
        print("------------------------------------------------")
        print("Algorithm Strategy:" + route.get_algorithm_name())
        print("Total Distance: " + str(route.get_distance()))
        print("Elevation Gain: " + str(route.get_total_gain()))
        print("Elevation Drop: " + str(route.get_total_drop()))

    def generate_paths(self, origin, destination, path_limit, elevation_strategy):
        # calculate shortest path
        self.set_shortest_route_object(destination)

        shortest_path_object = self.shortest_route_object.get_shortest_route(origin, destination)
        path_limit = path_limit / 100.0
        self.set_algorithm_object(shortest_path_object.get_starting_point(),
                                  shortest_path_object.get_ending_node(),
                                  shortest_path_object.get_shortest_path_distance(),
                                  path_limit,
                                  elevation_strategy)

        shortest_path_information = PathInformation()
        shortest_path_information.set_algorithm_name(SHORTEST)
        shortest_path_information.set_total_gain(
            self.algorithm_object.get_path_weight(shortest_path_object.get_shortest_path(), ELEVATION_GAIN))
        shortest_path_information.set_total_drop(
            self.algorithm_object.get_path_weight(shortest_path_object.get_shortest_path(), ELEVATION_DROP))
        shortest_path_information.set_path(shortest_path_object.get_shortest_route_lat_long())
        shortest_path_information.set_distance(shortest_path_object.get_shortest_path_distance())

        self.print_route_information(shortest_path_information)

        if path_limit == 0:
            return shortest_path_information, shortest_path_information

        elevation_route_information = self.algorithm_object.shortest_route()

        self.print_route_information(elevation_route_information)

        # If elevation route doesn't return a shortest path based on elevation requirements
        if (elevation_strategy == MAXIMIZE and elevation_route_information.get_total_gain() == float('-inf')) or (
                elevation_strategy == MINIMIZE and elevation_route_information.get_total_drop() == float('-inf')):
            elevation_route_information = PathInformation()

        elevation_route_information.set_path([[self.graph.nodes[route_node]['x'],
                                               self.graph.nodes[route_node]['y']]
                                              for route_node in elevation_route_information.get_path()])

        self.observer.update_notifier(shortest_path_information,
                                      elevation_route_information,
                                      get_address_from_coordinates(origin),
                                      get_address_from_coordinates(destination))