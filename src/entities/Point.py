class Vector:
    def __init__(self, vector=None):
        if vector is None:
            self.vector = []
        else:
            self.vector = vector

    @classmethod
    def toVector(cls, expression):
        return Vector(expression)

    def equalid_norm(self):
        """Вычисление евклидовой нормы вектора"""
        return sum(x ** 2 for x in self.vector) ** 0.5

    def scalar_multiply(self, scalar):
        """Умножение вектора на скаляр"""
        return Vector([scalar * x for x in self.vector])

    def __iter__(self):
        """Позволяет итерировать по элементам вектора"""
        return iter(self.vector)

    def __sub__(self, other):
        """
        Вычитание двух векторов
        :param other: Вектор, который вычитается из текущего
        """
        return Vector([a - b for a, b in zip(self.vector, other)])

    def append(self, value):
        self.vector.append(value)

    def __repr__(self):
        return f"Vector({self.vector})"

    def copy(self):
        return Vector(self.vector.copy())

    def __eq__(self, other):
        """Проверка на равенство векторов"""
        if isinstance(other, Vector):
            return self.vector == other.vector
        return False

    def __len__(self):
        return len(self.vector)

    def __getitem__(self, index):
        """Позволяет доступ к элементам по индексу: v[0], v[1]"""
        return self.vector[index]

    def __setitem__(self, index, value):
        """Позволяет изменять элементы по индексу: v[0] = 10"""
        self.vector[index] = value