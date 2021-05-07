class PathInformation:
    """
    This class initializes the path with default values and contains getter and setter methods for all path related attributes
    """
    def __init__(self):
        self.algorithm_name = "Empty"
        self.total_gain = 0
        self.total_drop = 0
        self.path = []
        self.distance = 0.0
        self.starting_node = None, None
        self.ending_node = None, None

    def set_algorithm_name(self, algorithm_name):
        """
        This method sets the algorithm name to the name that is  passed as the parameter to the method.
        Args:
            algorithm_name:

        Returns:

        """
        self.algorithm_name = algorithm_name

    def set_total_gain(self, total_gain):
        """
        This method sets the total gain to the value that is  passed as the parameter to the method.

        Args:
            total_gain:

        Returns:

        """
        self.total_gain = total_gain

    def set_total_drop(self, total_drop):
        """
        This method sets the total drop  to the value that is  passed as the parameter to the method.

        Args:
            total_drop:

        Returns:

        """
        self.total_drop = total_drop

    def set_path(self, path):
        """
        This method sets the path to the value that is  passed as the parameter to the method.

        Args:
            path:

        Returns:

        """
        self.path = path

    def set_distance(self, distance):
        """
        This method sets the distance  to the value that is  passed as the parameter to the method.

        Args:
            distance:

        Returns:

        """
        self.distance = distance

    def get_algorithm_name(self):
        """
        This is the getter method for fetching the algorithm name.

        Returns:The algorithm name

        """
        return self.algorithm_name

    def get_total_gain(self):
        """
        This is the getter method for fetching the total gain.

        Returns:The total gain

        """

        return self.total_gain

    def get_total_drop(self):
        """
        This is the getter method for fetching the total drop.

        Returns:The total drop

        """
        return self.total_drop

    def get_path(self):
        """
        This is the getter method for fetching the path information.

        Returns:The path information.

        """
        return self.path

    def get_distance(self):
        """
        This is the getter method for fetching the distance.

        Returns:Distance between two places.
        """
        return self.distance

    def set_starting_node(self, starting_node):
        """
        This method sets the starting node to the value that is  passed as the parameter to the method.

        Args:
            starting_node:

        Returns:

        """
        self.starting_node = starting_node

    def get_starting_node(self):
        """
        This is the getter method for fetching the starting node value.

        Returns:The starting node value

        """
        return self.starting_node

    def set_ending_node(self, ending_node):
        """
        This method sets the ending node to the value that is  passed as the parameter to the method.

        Args:
            ending_node:

        Returns:

        """
        self.ending_node = ending_node

    def get_ending_node(self):
        """
        This is the getter method for fetching the ending node value.

        Returns:The ending node value

        """
        return self.ending_node
