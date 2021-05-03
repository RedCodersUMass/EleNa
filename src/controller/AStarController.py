from src.controller.AbstractController import *
from src.constants.constants import *
from src.model.AStarRoute import AstarRoute


class AStarController(AbstractController):

    def __init__(self):
        self.model = None
        self.observer = None
        self.elevation_strategy = None
        self.start_point = None
        self.end_point = None
        self.path_limit = None

    def set_model(self, model):
        self.model = model

    def set_elevation_strategy(self, elevation_strategy):
        self.elevation_strategy = elevation_strategy

    def set_start_point(self, start_point):
        self.start_point = start_point

    def set_end_point(self, end_point):
        self.end_point = end_point

    def set_path_limit(self, path_limit):
        self.path_limit = path_limit

    def manipulate_model(self):
        self.model.set_algorithm(AstarRoute)
        self.model.generate_paths(self.start_point, self.end_point, self.path_limit, self.elevation_strategy)
