from abc import ABC, abstractmethod

class ViewInterface(ABC):
    @abstractmethod
    def add_iteration_info(self, iteration_info):
        pass

    @abstractmethod
    def get_params(self):
        pass

    @abstractmethod
    def set_surface(self, surface):
        pass