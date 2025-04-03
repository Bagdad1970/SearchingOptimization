from time import sleep

import src.math_functions as math_functions
from src.entities.point import Point
from src.function_from_str import function_from_str
from src.model.strategies.strategy_interface import StrategyInterface
from src.model.algorithm_observer import AlgorithmObserver


class GradientDescent(StrategyInterface):
    def __init__(self):
        super().__init__()
        self.algorithm_observer = None
        self.function = None  # Целевая функция
        self.point = None  # Начальная точка
        self.eps = 1e-6  # Общая точность
        self.eps1 = 1e-6  # Точность для градиента
        self.eps2 = 1e-6  # Точность для изменения точки
        self.step = 0.1  # Начальный шаг
        self.max_iteration = 100  # Максимальное количество итераций

    def set_algorithm_observer(self, algorithm_observer: AlgorithmObserver):
        self.algorithm_observer = algorithm_observer

    @staticmethod
    def initial_function():
        return '2*x1**2 + x1*x2 + x2**2'

    def set_params(self, function, **params):
        self.function = function_from_str(function)
        self.point = params.get('point', self.point)
        self.eps = params.get('epsilon', self.eps)
        self.eps1 = params.get('epsilon1', self.eps1)
        self.eps2 = params.get('epsilon2', self.eps2)
        self.step = params.get('step', self.step)
        self.max_iteration = params.get('max_iteration', self.max_iteration)

    @staticmethod
    def next_point(point: Point, gradient: Point, step: float):
        return point - gradient.scalar_multiply(step)

    def execute(self):
        current_iteration = 0

        while True:
            gradient = math_functions.gradient(function=self.function, point=self.point)

            gradient_norm = gradient.equalid_norm()
            if gradient_norm < self.eps1:
                stop_reason = "Норма градиента меньше заданного eps1"
                break

            if current_iteration >= self.max_iteration:
                stop_reason = "Достигнут предел итераций"
                break

            new_point = self.next_point(self.point, gradient, self.step)

            function_value_next_point, function_value_current_point = self.function(*new_point), self.function(*self.point)
            while function_value_next_point >= function_value_current_point:
                self.step /= 2
                new_point = self.next_point(self.point, gradient, self.step)
                function_value_next_point = self.function(*new_point)

            distance_points_norm = (new_point - self.point).equalid_norm()
            distance_functions_value = abs(self.function(*new_point) - self.function(*self.point))
            if distance_points_norm < self.eps2 and distance_functions_value < self.eps2:
                self.point = new_point
                stop_reason = "Расстояние между точками и значениями функций меньше заданного eps2"
                break
            else:
                self.point = new_point
                current_iteration += 1

            self.algorithm_observer.point_observer.notify_all(Point.full_point(self.point, self.function))

            iteration_info = f"Итерация {current_iteration}: точка ({self.point[0]:5f}, {self.point[1]:.5f}, {self.function(*self.point):.5f})"
            self.algorithm_observer.iteration_observer.notify_all(iteration_info)

        result = f"Результат: точка ({self.point[0]:5f}, {self.point[1]:.5f}, {self.function(*self.point):.5f})"
        self.algorithm_observer.iteration_observer.notify_all(result)

        self.algorithm_observer.stop_reason_observer.notify_all(stop_reason)