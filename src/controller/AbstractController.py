from abc import ABC, abstractmethod

class AbstractController(ABC):
    def __init__(self):
        self.model = None
        self.observer = None
        self.strategy = None

    @abstractmethod
    def set_model(self, model):
        pass

    @abstractmethod
    def set_strategy(self, strategy):
        pass

    @abstractmethod
    def manipulate_model(self):
        pass