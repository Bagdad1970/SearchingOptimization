from src.entities.Vector import Vector

def gradient(function, vector, h=1e-5):
    """
    Вычисляет градиент функции f в точке x методом конечных разностей.

    :param function: Функция, градиент которой нужно вычислить градиент
    :param x: Точка, в которой вычисляется градиент (список или массив)
    :param h: Шаг для метода конечных разностей
    :return: Градиент функции в точке x (список)
    """
    gradient = Vector()
    for i_coord in range(len(vector)):
        x_plus_h = vector.copy()
        x_minus_h = vector.copy()

        x_plus_h[i_coord] += h
        x_minus_h[i_coord] -= h

        partial_derivative = (function(x_plus_h) - function(x_minus_h)) / (2 * h)
        gradient.append(partial_derivative)

    return gradient