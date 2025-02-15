from abc import ABC, abstractmethod

class AlgorithmInterface(ABC):

    @abstractmethod
    def set_params(self, **params):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def surface_params(self) -> dict:
        pass