from src.entities.point import Point

def gradient(*, function, point: Point, h=1e-6):
    """
    Вычисляет градиент функции f в точке x методом конечных разностей.

    :param function: Функция, градиент которой нужно вычислить градиент
    :param point: Координаты точки
    :param x: Точка, в которой вычисляется градиент (список или массив)
    :param h: Шаг для метода конечных разностей
    :return: Градиент функции в точке x (список)
    """
    gradient = Point()
    for point_coord in range(len(point)):
        x_plus_h = point.copy()
        x_minus_h = point.copy()

        x_plus_h[point_coord] += h
        x_minus_h[point_coord] -= h

        partial_derivative = ( function(*x_plus_h) - function(*x_minus_h) ) / (2 * h)
        gradient.append(partial_derivative)

    return gradient