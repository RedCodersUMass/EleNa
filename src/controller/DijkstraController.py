from src.controller.AbstractController import *


class DijkstraController(AbstractController):

    def __init__(self):
        self.model = None
        self.observer = None
        self.strategy = None
        self.start_point = None
        self.end_point = None
        self.x = None

    def set_model(self, model):
        self.model = model

    def set_strategy(self, strategy):
        self.strategy  = strategy

    def set_start_point(self, start_point):
        self.start_point = start_point

    def set_end_point(self, end_point):
        self.end_point = end_point

    def set_x(self, x):
        self.x = x

    def manipulate_model(self):
        self.model.generate_paths(self.start_point, self.end_point, self.x, self.strategy)
