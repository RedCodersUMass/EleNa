from src.model.utils import *
from src.view.view import *
from src.model.shortestPath import ShortestPath
from src.model.GraphGenerator import GraphGenerator


class Model:
    def __init__(self):
        self.mapbox_api_key = None
        self.shortest_path_algorithm = None
        self.graph = None
        self.shortestPathObject = None
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

    def set_shortest_path_object(self, coord_end, x, elevation_flag):
        self.graph = GraphGenerator().generate_elevation_graph(coord_end)
        self.shortestPathObject = ShortestPath(self.graph, x=x, elevation_mode=elevation_flag)

    def generate_paths(self, origin, destination, x, elevation_flag):
        self.set_shortest_path_object(destination, x, elevation_flag)
        shortest_path, elev_path = self.shortestPathObject.get_shortest_path(origin, destination, x,
                                                                             elevation_mode=elevation_flag)
        self.observer.update_notifier(shortest_path, elev_path, get_address_from_coordinates(origin),
                                      get_address_from_coordinates(destination))
