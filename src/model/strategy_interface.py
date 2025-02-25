from abc import ABC, abstractmethod

class StrategyInterface(ABC):

    @abstractmethod
    def set_params(self, function, **params):
        pass

    @abstractmethod
    def execute(self):
        pass