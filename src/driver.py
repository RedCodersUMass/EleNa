from flask import Flask, request, render_template
from src.model.model import *
from src.view.view import View
from src.controller.AStarController import *
from src.controller.DijkstraController import *
from src.constants.constants import *
import json

ACCESS_KEY = 'pk.eyJ1IjoibXRhayIsImEiOiJja25wNmdyMTMxYm9tMm5wZTlha2lhcmFnIn0.JsFh89MfCIDr32o-1OHmdA'
static_folder = "./view/static"
template_folder = "./view/templates"
static_url_path = ''
app = Flask(__name__, static_folder=static_folder, template_folder=template_folder, static_url_path=static_url_path)
app.config.from_object(__name__)
app.config.from_envvar('APP_CONFIG_FILE', silent=True)


@app.route('/view')
def client():
    return render_template(
        'view.html',
        ACCESS_KEY=ACCESS_KEY
    )


@app.route('/path_via_pointers', methods=['POST'])
def get_route():
    json_output = request.get_json(force=True)
    print('Request - ',json_output)
    origin_coords = json.loads(json_output['origin_coords'])
    destination_coords = json.loads(json_output['dest_coords'])
    origin_point = (origin_coords['lat'], origin_coords['lng'])
    destination_point = (destination_coords['lat'], destination_coords['lng'])
    path_limit = float(json_output['elevation_percent'])
    elevation_strategy = MAXIMIZE #json_output['min_max'] #TODO
    algorithm = json_output['algorithm']
    model = Model()
    view = View()
    model.register_observer(view)
    if algorithm == "AStar":
        controller = AStarController()
    else:
        controller = DijkstraController()
    controller.set_model(model)
    controller.set_start_point(origin_point)
    controller.set_end_point(destination_point)
    controller.set_path_limit(path_limit)
    controller.set_elevation_strategy(elevation_strategy)
    controller.manipulate_model()
    return view.get_output_json()
