from abc import ABC, abstractmethod


class AbstractController(ABC):
    """
    This is abstract controller which has functionality that needs to be implemented by children classes
    """
    def __init__(self):
        self.model = None
        self.observer = None
        self.elevation_strategy = None

    @abstractmethod
    def set_model(self, model):
        pass

    @abstractmethod
    def set_elevation_strategy(self, elevation_strategy):
        pass

    @abstractmethod
    def manipulate_model(self):
        pass
