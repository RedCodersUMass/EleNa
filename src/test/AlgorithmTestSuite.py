import unittest
import sys
import unittest

from geopy.geocoders import Nominatim

from src.controller import *
from src.model.GraphGenerator import *
from src.model.AStarRoute import *
from src.model.DijkstraRoute import *
from src.model.ShortestRoute import *
from src.model.utils import *
import osmnx as ox
import json
from src.driver import *
from src.model.PathInformation import PathInformation


class AlgorithmTestSuite(unittest.TestCase):
    """
    This test suite contains unit test cases to check the graph using small graphs which could be visualized.
    It also analyzes the algorithms, dijkstra and star, and compares them using various values of extra path limit.
    """
    G = None

    @classmethod
    def setUpClass(self):
        """
        This is the setup method called before running the test cases once.
        Returns:

        """
        G = nx.Graph()
        # Create toy graph with nodes 0-5
        [G.add_node(i, elevation=0.0) for i in range(5)]
        edgeList = [(0, 1, 7), (1, 2, 3.0), (0, 3, 5), (3, 4, 4.0), (4, 2, 10)]
        elevList = [(0, 1, 0.0), (1, 2, 1.0), (0, 3, 3.0), (3, 4, 1.0), (4, 2, -3.0)]
        absElevList = [(0, 1, 0.0), (1, 2, 1.0), (0, 3, 3.0), (3, 4, 1.0), (4, 2, 3.0)]
        G.add_weighted_edges_from(edgeList)
        G.add_weighted_edges_from(elevList, weight="grade")
        G.add_weighted_edges_from(absElevList, weight="grade_abs")
        elev = [0.0, 0.0, 1.0, 3.0, 4.0]
        for i, e in enumerate(elev):
            G.nodes[i]["elevation"] = e
        self.G = G


    def test_get_graph(self):
        """
        This test case checks if the graph object is properly loaded.
        Returns:

        """
        destination = (42.389747, -72.528293)
        graph_obj = GraphGenerator()
        graph_instance = graph_obj.generate_elevation_graph(destination)
        assert isinstance(graph_instance, nx.classes.multidigraph.MultiDiGraph)

    def test_convert_address_to_coordinates(self):
        """
        This method checks the google address to coordinate api.
        Returns:

        """
        address = "UMass Amherst"
        x, y = convert_address_to_coordinates(address)
        assert isinstance(x, float)
        assert isinstance(y, float)

    def test_convert_coordinates_to_address(self):
        """
        This method checks the api to convert coordinates to human readable address
        Returns:

        """
        location = (42.3867637, -72.5322402)
        address = get_address_from_coordinates(location)
        assert 'University of Massachusetts Amherst' in address

    def test_weight_function(self):
        """
        This method checks if the utils calculate the weight between two nodes correctly.
        Returns:

        """
        weight = get_weight(self.G, 1, 2, "normal")
        assert weight == 3.0

    def test_get_path_weight(self):
        """
        This method checks if the utils calculate the sum of the weights on a route correctly.
        Returns:

        """
        route = [0, 1, 2, 4]
        weight = get_path_weight(self.G, route, "normal")
        assert weight == 20.0

    def test_get_path_elevation(self):
        """
        This method chcks if the utils calculate the sum of the elevations on a route correctly.
        Returns:

        """
        route = [0, 1, 2, 4]
        weight = get_path_weight(self.G, route, "elevation_gain")
        assert weight == 4.0

    def test_astar_shortest_path(self):
        """
        This test case checks if the path returned by astar has lesser elevation than the shortest path.
        Returns:

        """
        destination = (42.3867637, -72.5322402)
        start = (42.3978, -72.5147)
        path_limit = 50
        elevation_strategy = 'min'
        controller = AStarController()
        model = Model()
        view = View()
        model.register_observer(view)
        controller.set_model(model)
        controller.set_start_point(start)
        controller.set_end_point(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation_strategy)
        controller.manipulate_model()
        out_json = json.loads(view.get_output_json())
        shortest_path_dist = out_json['shortDist']
        elev_path_dist = out_json['elev_path_dist']
        shortest_path_elev = out_json['gainShort']
        elev_path_gain = out_json['elev_path_gain']
        assert elev_path_dist <= (1+ path_limit/100) * shortest_path_dist
        assert elev_path_gain <= shortest_path_elev

    def test_dijkstra_shortest_path(self):
        """
        This method checks if the path returned by dijkstra has lesser elevation than the shortest path.
        Returns:

        """
        destination = (42.3867637, -72.5322402)
        start = (42.3978, -72.5147)
        path_limit = 50
        elevation_strategy = 'min'
        controller = DijkstraController()
        model = Model()
        view = View()
        model.register_observer(view)
        controller.set_model(model)
        controller.set_start_point(start)
        controller.set_end_point(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation_strategy)
        controller.manipulate_model()
        out_json = json.loads(view.get_output_json())
        shortest_path_dist = out_json['shortDist']
        elev_path_dist = out_json['elev_path_dist']
        shortest_path_elev = out_json['gainShort']
        elev_path_gain = out_json['elev_path_gain']
        assert elev_path_dist <= (1+ path_limit/100) * shortest_path_dist
        assert elev_path_gain <= shortest_path_elev

    def test_astar_max_elevation(self):
        """
        This test case checks if the path returned by astar has greater elevation than the shortest path.
        Returns:

        """
        start = (42.3867637, -72.5322402)
        destination = (42.3978, -72.5147)
        path_limit = 50
        elevation_strategy = 'max'
        controller = AStarController()
        model = Model()
        view = View()
        model.register_observer(view)
        controller.set_model(model)
        controller.set_start_point(start)
        controller.set_end_point(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation_strategy)
        controller.manipulate_model()
        out_json = json.loads(view.get_output_json())
        shortest_path_dist = out_json['shortDist']
        elev_path_dist = out_json['elev_path_dist']
        shortest_path_elev = out_json['gainShort']
        elev_path_gain = out_json['elev_path_gain']
        assert elev_path_dist <= (1+ path_limit/100) * shortest_path_dist
        assert elev_path_gain >= shortest_path_elev

    def test_dijkstra_max_elevation(self):
        """
        This method checks if the path returned by dijkstra has greater elevation than the shortest path.
        Returns:

        """
        start = (42.3867637, -72.5322402)
        destination = (42.3978, -72.5147)
        path_limit = 50
        elevation_strategy = 'max'
        controller = DijkstraController()
        model = Model()
        view = View()
        model.register_observer(view)
        controller.set_model(model)
        controller.set_start_point(start)
        controller.set_end_point(destination)
        controller.set_path_limit(path_limit)
        controller.set_elevation_strategy(elevation_strategy)
        controller.manipulate_model()
        out_json = json.loads(view.get_output_json())
        shortest_path_dist = out_json['shortDist']
        elev_path_dist = out_json['elev_path_dist']
        shortest_path_elev = out_json['gainShort']
        elev_path_gain = out_json['elev_path_gain']
        assert elev_path_dist <= (1+ path_limit/100) * shortest_path_dist
        assert elev_path_gain >= shortest_path_elev

if __name__ == '__main__':
    unittest.main()
