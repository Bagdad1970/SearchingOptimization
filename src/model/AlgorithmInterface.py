from abc import ABC, abstractmethod

class AlgorithmInterface(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_graph(self):
        pass

    @abstractmethod
    def get_point(self):
        pass