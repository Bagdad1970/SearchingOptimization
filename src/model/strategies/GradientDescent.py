import src.math_functions as math_functions
from src.entities.Point import Point
from src.model.AlgorithmInterface import AlgorithmInterface
from src.model.Observer import Observer
import numpy as np
import pyqtgraph.opengl as gl

class GradientDescent(Observer, AlgorithmInterface):
    def __init__(self):
        super().__init__()
        self.function = None  # Целевая функция
        self.point = None  # Начальная точка
        self.eps = 1e-6  # Общая точность
        self.eps1 = 1e-6  # Точность для градиента
        self.eps2 = 1e-6  # Точность для изменения точки (можно убрать)
        self.step = 0.01  # Начальный шаг
        self.current_iteration = 0
        self.max_iteration = 100  # Максимальное количество итераций

    def set_params(self, **params):
        self.function = params['function']  # Целевая функция
        self.point = params['point']  # Начальная точка
        self.eps = params['eps']  # Общая точность
        self.eps1 = params['eps1']  # Точность для градиента
        self.eps2 = params['eps2']  # Точность для изменения точки (можно убрать)
        self.step = params['step']  # Начальный шаг
        self.max_iteration = params['max_iteration']  # Максимальное количество итераций

    def notify_all_about_new_point(self):
        pass

    def surface_params(self) -> dict:
        # Данные для графика
        x = np.linspace(-20, 20, 100)
        y = np.linspace(-20, 20, 100)
        function = lambda x, y: (x ** 2) + (y ** 2) if self.function is None else self.function
        return {'x': x, 'y': y, 'function': function}

    @staticmethod
    def next_point(point: Point, gradient: Point, step: float):
        return point - gradient.scalar_multiply(step)

    def execute(self) -> Point:
        while True:
            gradient = math_functions.gradient(function=self.function, point=self.point)

            gradient_norm = gradient.equalid_norm()
            if gradient_norm < self.eps1:
                break  # Остановка по норме градиента

            if self.current_iteration >= self.max_iteration:
                break

            # Обновление точки
            new_point = self.next_point(self.point, gradient, self.step)

            # Проверка уменьшения функции, если нет — уменьшаем шаг
            function_value_next_point, function_value_current_point = self.function(new_point), self.function(self.point)
            while function_value_next_point >= function_value_current_point:
                self.step /= 2
                new_point = self.next_point(self.point, gradient, self.step)
                function_value_next_point = self.function(new_point)

            "Где-то поставить notify_all_about_new_point()"

            distance_points_norm = (new_point - self.point).equalid_norm()
            distance_functions_value = abs(self.function(new_point) - self.function(self.point))
            if distance_points_norm < self.eps2 and distance_functions_value < self.eps2:
                self.point = new_point
                break # Остановка по изменению точки
            else:
                self.current_iteration += 1
                self.point = new_point

            # Вывод информации об итерации
            print(f"Iteration {self.current_iteration}: x = {[round(p, 5) for p in self.point]}, f(x) = {self.function(self.point):.8f}")

            "Добавить вывод из-за чего остановлено выполнение"

        # Итоговый результат
        print(f"\nResult: x = {[round(p, 5) for p in self.point]}, f(x) = {self.function(self.point):.8f}")
        return self.point

strategy = GradientDescent()
print(strategy)

"""
def example_function(point: Point):
    x, y = point
    return 2 * (x ** 2) + x * y + (y ** 2)

if __name__ == "__main__":
    initial_point = [0.5, 1]
    optimizer = GradientDescent(function=example_function, point=initial_point, eps1=0.1, eps2=0.15, step=0.1, max_iteration=60)
    print(optimizer.execute())

"""