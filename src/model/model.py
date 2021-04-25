from src.model.utils import *
from src.view.view import *
from src.model.ShortestRoute import ShortestRoute
from src.model.GraphGenerator import GraphGenerator


class Model:
    def __init__(self):
        self.mapbox_api_key = None
        self.shortest_path_algorithm = None
        self.graph = None
        self.shortestRouteObject = None
        self.observer = None
        self.algorithm = None

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

    def set_shortest_path_object(self, coord_end):
        self.graph = GraphGenerator().generate_elevation_graph(coord_end)
        self.shortestRouteObject = ShortestRoute(self.graph)

    def generate_paths(self, origin, destination, x, strategy):
        
        self.set_shortest_path_object(destination)

        shortest_route = self.shortestRouteObject.get_shortest_route(origin, destination)
        
        self.observer.update_notifier(shortest_route, shortest_route, get_address_from_coordinates(origin),
                                      get_address_from_coordinates(destination))
