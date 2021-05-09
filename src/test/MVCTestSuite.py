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


class MVCTestSuite(unittest.TestCase):
    """
    This class contains unittest cases to check the working of the model view controller architecture.
    """
    def test_dijkstra_controller(self):
        """
        This test case checks if the dijkstra controller makes the required changes to the model.
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
        assert model.algorithm == DijkstraRoute

    def test_astar_controller(self):
        """
        This method checks if the astar controller makes the required changes to the model.
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
        assert model.algorithm == AstarRoute

if __name__ == '__main__':
    unittest.main()
