import json
from src.view.utils import *
from src.model.model import *


class View:
    """
    This class is the View class. Formats the output JSON object.
    """
    def __init__(self):
        """
        View class constructor method.
        """
        self.output_json = {}

    def update_notifier(self, shortest_route=None, elevation_route=None, starting_point=None, ending_point=None):
        self.output_json = {ELEV_PATH_ROUTE: update_route_json(elevation_route.get_path()),
                            SHORTEST_PATH_ROUTE: update_route_json(shortest_route.get_path()),
                            SHORTEST_PATH_DIST: shortest_route.get_distance(),
                            SHORTEST_PATH_GAIN: shortest_route.get_total_gain(),
                            SHORTEST_PATH_DROP: shortest_route.get_total_drop(),
                            ORIGIN: starting_point,
                            DESTINATION: ending_point,
                            ELEV_PATH_DIST: elevation_route.get_distance(),
                            ELEV_PATH_GAIN: elevation_route.get_total_gain(),
                            ELEV_PATH_DROP: elevation_route.get_total_drop()}
        if len(elevation_route.get_path()) == 0:
            self.output_json[BOOL_POP] = 1
        else:
            self.output_json[BOOL_POP] = 2

    def get_output_json(self):
        """
        Returns output JSON object.

        Returns:
            JSON object
        """
        print('Sending output - ', self.output_json)
        return json.dumps(self.output_json)
