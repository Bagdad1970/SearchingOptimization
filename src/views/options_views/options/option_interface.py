from abc import ABC, abstractmethod
from collections.abc import Callable
from src.entities.point import Point


class OptionInterface(ABC):

    def get_point(self, function: Callable=None):
        if function is None:
            return Point([0, 0, 0])
        return Point([0, 0,
                      function(*Point([0, 0]))
                      ])

    @abstractmethod
    def get_params(self):
        raise NotImplementedError