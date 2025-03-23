import math
import numpy as np


class Point:
    """
    Represents coordinate point in n-dimensional space
    """

    def __init__(self, point=None):
        self.point = point if point is not None else []

    def create_points_array(self, *, x_length: float, y_length: float) -> tuple:
        x_left_length, x_right_length = math.ceil(
            (self.point[0] - x_length) / 2
        ), math.ceil((self.point[0] + x_length) / 2)
        y_left_length, y_right_length = math.ceil(
            (self.point[1] - y_length) / 2
        ), math.ceil((self.point[1] + y_length) / 2)
        return (
            np.linspace(x_left_length, x_right_length, 100),
            np.linspace(y_left_length, y_right_length, 100),
        )

    @classmethod
    def full_point(cls, point, function):
        function_value = function(*point)
        return Point([*point, function_value])

    def get_point(self):
        return self.point

    def equalid_norm(self):
        return sum(x**2 for x in self.point) ** 0.5

    def scalar_multiply(self, scalar):
        """Умножение вектора на скаляр"""
        return Point([scalar * x for x in self.point])

    def __add__(self, other):
        return Point(
            [
                self.point[i] + other[i]
                for i in range(min(len(self.point), len(other.point)))
            ]
        )

    def __iter__(self):
        """Позволяет итерировать по элементам вектора"""
        return iter(self.point)

    def __sub__(self, other):
        """
        Substract first point from second
        :param other: Substracted point
        """
        return Point([a - b for a, b in zip(self.point, other)])

    def append(self, value):
        self.point.append(value)

    def copy(self):
        return Point(self.point.copy())

    def __eq__(self, other):
        """Проверка на равенство векторов"""
        if isinstance(other, Point):
            return self.point == other.point
        return False

    def __len__(self):
        return len(self.point)

    def __getitem__(self, index):
        return self.point[index]

    def __setitem__(self, index, value):
        self.point[index] = value

    def __repr__(self):
        return f"Point({self.point!r})"
