class PathInformation:
    def __init__(self):
        self.algorithm_name = "Empty"
        self.total_gain = 0
        self.total_drop = 0
        self.path = []
        self.distance = 0.0
        self.starting_node = None, None
        self.ending_node = None, None

    def set_algorithm_name(self, algorithm_name):
        self.algorithm_name = algorithm_name

    def set_total_gain(self, total_gain):
        self.total_gain = total_gain

    def set_total_drop(self, total_drop):
        self.total_drop = total_drop

    def set_path(self, path):
        self.path = path

    def set_distance(self, distance):
        self.distance = distance

    def get_algorithm_name(self):
        return self.algorithm_name

    def get_total_gain(self):
        return self.total_gain

    def get_total_drop(self):
        return self.total_drop

    def get_path(self):
        return self.path

    def get_distance(self):
        return self.distance

    def set_starting_node(self, starting_node):
        self.starting_node = starting_node

    def get_starting_node(self):
        return self.starting_node

    def set_ending_node(self, ending_node):
        self.ending_node = ending_node

    def get_ending_node(self):
        return self.ending_node
