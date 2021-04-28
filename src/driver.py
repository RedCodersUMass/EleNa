from flask import Flask, request, render_template
from src.model.model import *
from src.view.view import View
from src.controller.AStarController import *
from src.controller.DijkstraController import *
from src.constants.constants import *

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
    origin_point = (json_output['start_location']['lat'], json_output['start_location']['lng'])
    destination_point = (json_output['end_location']['lat'], json_output['end_location']['lng'])
    x = 20#json_output['x']
    elevation_strategy = json_output['min_max']
    algorithm = DIJKSTRA
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
    controller.set_x(x)
    controller.set_elevation_strategy(elevation_strategy)
    controller.manipulate_model()
    return view.get_output_json()
