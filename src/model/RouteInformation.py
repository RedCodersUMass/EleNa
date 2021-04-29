class RouteInformation:
    def __init__(self):
        self.starting_node = None
        self.ending_node = None
        # networkx.algorithms.shortest_paths.generic.shortest_path
        self.shortest_path = None
        self.shortest_route_lat_long = None
        self.shortest_path_distance = None

    def set_starting_point(self, starting_point):
        self.starting_point = starting_point

    def set_ending_node(self, ending_node):
        self.ending_node = ending_node

    def set_shortest_path(self, shortest_path):
        self.shortest_path = shortest_path

    def set_shortest_route_lat_long(self, shortest_route_lat_long):
        self.shortest_route_lat_long = shortest_route_lat_long

    def set_shortest_path_distance(self, shortest_path_distance):
        self.shortest_path_distance = shortest_path_distance

    def get_starting_point(self):
        return self.starting_point

    def get_ending_node(self):
        return self.ending_node

    def get_shortest_path(self):
        return self.shortest_path

    def get_shortest_route_lat_long(self):
        return self.shortest_route_lat_long

    def get_shortest_path_distance(self):
        return self.shortest_path_distance