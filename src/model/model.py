from src.model.GraphGenerator import GraphGenerator
from src.model.ShortestRoute import ShortestRoute
from src.model.utils import get_address_from_coordinates
from src.view.view import *
from src.constants.constants import *
from src.model.PathInformation import PathInformation
from src.model.DijkstraRoute import DijkstraRoute
from src.model.AStarRoute import AstarRoute
from src.model.utils import get_path_weight

class Model:
    """
    This class initializes critical parameters such the graph,the algorithm,the path_limit  etc.It contains methods to register the
    observer,set the algorithm,set the algorithm object,print the route information etc and also it notifies the observers.
    """
    def __init__(self):
        """
        This method initializes the  route and algorithm attributes
        """
        self.mapbox_api_key = None
        self.graph = None
        self.shortest_route_object = None
        self.shortest_path_information = None
        self.elevation_route_object = None
        self.elevation_path_information = None
        self.observer = None
        self.algorithm = None
        self.algorithm_object = None
        self.path_limit = None
        self.elevation_strategy = None

    def register_observer(self, observer):
        """
        This method registers the observer.

        Args:
            observer:

        Returns:

        """
        self.observer = observer

    def set_algorithm(self, algorithm):
        """
        This is the setter method for the algorithm.

        Args:
            algorithm:

        Returns:

        """

        self.algorithm = algorithm

    def get_mapbox_api(self):
        """
        This is the method for fetching the mapbox_api key.

        Returns:
        The mapbox_api_key.

        """
        return self.mapbox_api_key

    def set_mapbox_api(self, api_key):
        """
        This is the setter method for setting the value of the mapbox_api key.

        Args:
            api_key:

        Returns:

        """

        self.mapbox_api_key = api_key

    def set_shortest_route_object(self, coord_start, coord_end):
        """
        This method sets the shortest path based on the starting and ending coordinates.

        Args:
            coord_start:
            coord_end:

        Returns:

        """
        self.graph = GraphGenerator().generate_elevation_graph(coord_end)
        self.shortest_route_object = ShortestRoute(self.graph)
        self.shortest_path_information = self.shortest_route_object.get_shortest_route(coord_start, coord_end)

    def set_algorithm_object(self):
        """
        This method sets the algorithm object by passing the graph,distance,path_limit,elevation strategy,starting node,ending node
        and gain values to the algorithm.

        Returns:

        """

        self.algorithm_object = self.algorithm(self.graph,
                                               self.shortest_path_information.get_distance(),
                                               self.path_limit,
                                               self.elevation_strategy,
                                               self.shortest_path_information.get_starting_node(),
                                               self.shortest_path_information.get_ending_node(),
                                               self.shortest_path_information.get_total_gain())

    def print_route_information(self, route):
        """
        This method prints the route information to the terminal.
        Args:
            route:

        Returns:

        """
        print("#")
        print("Algorithm Strategy:" + route.get_algorithm_name())
        print("Total Distance: " + str(route.get_distance()))
        print("Elevation Gain: " + str(route.get_total_gain()))
        print("#")

    def generate_paths(self, origin, destination, path_limit, elevation_strategy):
        """
        This method generates the shortest path based on the elevation strategy and the path limit specified.
        Args:
            origin:
            destination:
            path_limit:
            elevation_strategy:

        Returns:

        """
        # calculate shortest path
        self.set_shortest_route_object(origin, destination)
        self.print_route_information(self.shortest_path_information)
        if path_limit == 0:
            self.observer.update_notifier(self.shortest_path_information,
                                          self.shortest_path_information,
                                          get_address_from_coordinates(origin),
                                          get_address_from_coordinates(destination))
            return

        self.path_limit = path_limit / 100.0
        self.elevation_strategy = elevation_strategy

        self.set_algorithm_object()
        self.elevation_path_information = self.algorithm_object.get_shortest_route()

        self.print_route_information(self.elevation_path_information)

        self.observer.update_notifier(self.shortest_path_information,
                                      self.elevation_path_information,
                                      get_address_from_coordinates(origin),
                                      get_address_from_coordinates(destination))