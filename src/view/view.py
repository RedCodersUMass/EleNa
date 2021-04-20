import json
from src.constants.constants import *
from src.view.utils import *
from flask import Flask, request, render_template
from src.model.model import *


class View:
    def __init__(self):
        self.output_json = {}

    def update_notifier(self, sPath=None, ePath=None, start=None, end=None):
        self.output_json = {ELEV_PATH_ROUTE: update_route_json(ePath[0]),
                            SHORTEST_PATH_ROUTE: update_route_json(sPath[0]),
                            SHORTEST_PATH_DIST: sPath[1],
                            SHORTEST_PATH_GAIN: sPath[2],
                            SHORTEST_PATH_DROP: sPath[3],
                            ORIGIN: start,
                            DESTINATION: end,
                            ELEV_PATH_DIST: ePath[1],
                            ELEV_PATH_GAIN: ePath[2],
                            ELEV_PATH_DROP: ePath[3]}
        if len(ePath[0]) == 0:
            self.output_json[BOOL_POP] = 1
        else:
            self.output_json[BOOL_POP] = 2

    def get_output_json(self):
        return json.dumps(self.output_json)
