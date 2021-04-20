import pickle as pkl
import numpy as np
from haversine import haversine, Unit
import osmnx as ox
import os


class GraphGenerator:

    def __init__(self):
        self.graph = None
        self.google_map_api_key = "AIzaSyDi1gpXppDygu9VMC5bXRNB7SdpSuGDXUw"
        # Centre point is the location of UMass Amherst
        self.centre_point = (42.3867637, -72.5322402)
        self.offline_map_location = "openstreetmapoffline.p"

    def cache_map(self):
        # This method fetched the map from OSMNX and adds elevation attributes
        print("Downloading the Map")
        self.graph = ox.graph_from_point(self.centre_point, dist=15000, network_type='walk')
        # After creating the graph, add the elevation attributes
        self.graph = ox.add_node_elevations(self.graph, api_key=self.google_map_api_key)
        # Saving the graph which had been created.
        pkl.dump(self.graph, open(self.offline_map_location, "wb"))
        print("The Graph has been saved")

    def generate_elevation_graph(self, dest_node):
        # Updates the graph with distance from end point and returns it.
        print("Trying to load offline map....", self.offline_map_location)
        if os.path.exists(self.offline_map_location):
            self.graph = pkl.load(open(self.offline_map_location, "rb"))
            print("Offline Map loaded!")
        else:
            print("No offline map found.")
            self.cache_map()

        # Graph is updated with Distance from all nodes in the graph to the final destination
        end_node = self.graph.nodes[ox.get_nearest_node(self.graph, point=dest_node)]
        for node, data in self.graph.nodes(data=True):
            end_x = end_node['x']
            end_y = end_node['y']
            node_x = self.graph.nodes[node]['x']
            node_y = self.graph.nodes[node]['y']
            data['dist_from_dest'] = haversine((end_x, end_y), (node_x, node_y), unit=Unit.METERS)
        return self.graph
