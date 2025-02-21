import numpy as np

class Point:
    def __init__(self, point=None):
        if point is None:
            self.point = []
        else:
            self.point = point

    def create_points_array(self) -> tuple:
        x, y = self.point[0], self.point[1]
        return np.linspace(x-20, x+20, 100), np.linspace(y-20, y+20, 100)

    def get_point(self):
        return self.point

    @classmethod
    def toPoint(cls, expression):
        return Point(expression)

    def equalid_norm(self):
        """Вычисление евклидовой нормы вектора"""
        return sum(x ** 2 for x in self.point) ** 0.5

    def scalar_multiply(self, scalar):
        """Умножение вектора на скаляр"""
        return Point([scalar * x for x in self.point])

    def __iter__(self):
        """Позволяет итерировать по элементам вектора"""
        return iter(self.point)

    def __sub__(self, other):
        """
        Вычитание двух векторов
        :param other: Вектор, который вычитается из текущего
        """
        return Point([a - b for a, b in zip(self.point, other)])

    def append(self, value):
        self.point.append(value)

    def __repr__(self):
        return f"Point({self.point})"

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
        """Позволяет доступ к элементам по индексу: v[0], v[1]"""
        return self.point[index]

    def __setitem__(self, index, value):
        """Позволяет изменять элементы по индексу: v[0] = 10"""
        self.point[index] = value