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

        Args:
            algorithm_name:

        Returns:
            Nothing,this is a setter method for the algorithm name.

        """
        self.algorithm_name = algorithm_name

    def set_total_gain(self, total_gain):
        """

        Args:
            total_gain:

        Returns:
            Nothing,this is a setter method for the total gain.

        """
        self.total_gain = total_gain

    def set_total_drop(self, total_drop):
        """

        Args:
            total_drop:

        Returns:
            Nothing,this is a setter method for the total drop.

        """
        self.total_drop = total_drop

    def set_path(self, path):
        """

        Args:
            path:

        Returns:
            Nothing,this is a setter method for the path.

        """
        self.path = path

    def set_distance(self, distance):
        """

        Args:
            distance:

        Returns:
             Nothing,this is a setter method for the distance.

        """
        self.distance = distance

    def get_algorithm_name(self):
        """

        Returns:The algorithm name

        """
        return self.algorithm_name

    def get_total_gain(self):
        """

        Returns:The total gain

        """

        return self.total_gain

    def get_total_drop(self):
        """

        Returns:The total drop

        """
        return self.total_drop

    def get_path(self):
        """

        Returns:The path information.

        """
        return self.path

    def get_distance(self):
        """

        Returns:Distance between two places.

        """
        return self.distance

    def set_starting_node(self, starting_node):
        """

        Args:
            starting_node:

        Returns:
        Nothing,this sets the starting node value.
        """
        self.starting_node = starting_node

    def get_starting_node(self):
        """

        Returns:The starting node value

        """
        return self.starting_node

    def set_ending_node(self, ending_node):
        """

        Args:
            ending_node:

        Returns:
            Nothing,this sets the ending node value.

        """
        self.ending_node = ending_node

    def get_ending_node(self):
        """

        Returns:The ending node value

        """
        return self.ending_node
