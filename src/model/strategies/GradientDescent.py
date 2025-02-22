import src.math_functions as math_functions
from src.entities.Point import Point
from src.model.AlgorithmInterface import AlgorithmInterface
from src.model.PointObserver import PointObserver

class GradientDescent(PointObserver, AlgorithmInterface):
    def __init__(self):
        super().__init__()
        self.function = None  # Целевая функция
        self.point = None  # Начальная точка
        self.eps = 1e-6  # Общая точность
        self.eps1 = 1e-6  # Точность для градиента
        self.eps2 = 1e-6  # Точность для изменения точки (можно убрать)
        self.step = 0.01  # Начальный шаг
        self.max_iteration = 100  # Максимальное количество итераций

    def set_params(self, function, **params):
        self.function = function  # Целевая функция
        self.point = params['point']
        self.eps = params['epsilon']
        self.eps1 = params['epsilon1']
        self.eps2 = params['epsilon2']
        self.step = params['step']
        self.max_iteration = params['max_iteration']

    @staticmethod
    def next_point(point: Point, gradient: Point, step: float):
        return point - gradient.scalar_multiply(step)

    def execute(self):
        current_iteration = 0
        finish_status = None

        while True:
            gradient = math_functions.gradient(function=self.function, point=self.point)

            gradient_norm = gradient.equalid_norm()
            if gradient_norm < self.eps1:
                break

            if current_iteration >= self.max_iteration:
                break

            new_point = self.next_point(self.point, gradient, self.step)

            # Проверка уменьшения функции, если нет — уменьшаем шаг
            function_value_next_point, function_value_current_point = self.function(*new_point), self.function(*self.point)
            while function_value_next_point >= function_value_current_point:
                self.step /= 2
                new_point = self.next_point(self.point, gradient, self.step)
                function_value_next_point = self.function(*new_point)

            self.notify_about_new_point(self.function, new_point)

            distance_points_norm = (new_point - self.point).equalid_norm()
            distance_functions_value = abs(self.function(*new_point) - self.function(*self.point))
            if distance_points_norm < self.eps2 and distance_functions_value < self.eps2:
                self.point = new_point
                break
            else:
                self.point = new_point
                current_iteration += 1

            iteration_info = f"Итерация {current_iteration}: X {[round(p, 5) for p in self.point]}, f(X) = {self.function(*self.point):.6f}"
            self.notify_about_new_iteration(iteration_info)

            "Добавить вывод из-за чего остановлено выполнение"

        # Итоговый результат

        result = f"Результат: X {[round(p, 5) for p in self.point]}, f(X) = {self.function(*self.point):.6f}"
        self.notify_about_new_iteration(result)