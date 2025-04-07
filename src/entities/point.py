import math
import numpy as np
from collections import UserList


class Point(UserList):
    """
    Represents coordinate point in n-dimensional space
    """

    def __init__(self, point=None):
        super().__init__(point if point is not None else [])

    def create_points_array(self, *, x_length: float, y_length: float) -> tuple:
        x_left_length, x_right_length = math.ceil(
            (self.data[0] - x_length) / 2
        ), math.ceil((self.data[0] + x_length) / 2)
        y_left_length, y_right_length = math.ceil(
            (self.data[1] - y_length) / 2
        ), math.ceil((self.data[1] + y_length) / 2)
        return (
            np.linspace(x_left_length, x_right_length, 100),
            np.linspace(y_left_length, y_right_length, 100),
        )

    @classmethod
    def full_point(cls, point, function):
        function_value = function(*point)
        return Point([*point, function_value])

    def get_point(self):
        return self.data

    def equalid_norm(self):
        return sum(x**2 for x in self.data) ** 0.5

    def scalar_multiply(self, scalar):
        """Умножение вектора на скаляр"""
        return Point([scalar * x for x in self.data])

    def __add__(self, other):
        return Point(
            [
                self.data[i] + other[i]
                for i in range(min(len(self.data), len(other)))
            ]
        )

    def __sub__(self, other):
        """
        Substract first point from second
        :param other: Substracted point
        """
        return Point([a - b for a, b in zip(self.data, other)])

    def copy(self):
        return Point(self.data.copy())

    def __eq__(self, other):
        """Проверка на равенство векторов"""
        if isinstance(other, Point):
            return self.data == other.data
        return False

    def __repr__(self):
        return f"Point({self.data!r})"