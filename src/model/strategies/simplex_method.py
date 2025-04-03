from src.entities.point import Point
from src.model.strategies.strategy_interface import StrategyInterface
import sys
sys.path.append("/home/bagdad/study/searchingOptimization/quadratic_simplex")

import quadratic_simplex
from quadratic_simplex.limitation import Limitation
from src.function_from_str import function_from_str


class SimplexMethod(StrategyInterface):
    def __init__(self):
        super().__init__()

        self.fitness_function = None
        self.limitations = None
        self.algorithm_observer = None

    def set_params(self, function: str, **params):
        self.fitness_function = function
        self.limitations = params['limitations']

    @staticmethod
    def initial_function():
            return '2*x1**2 + 2*x1*x2 + 2*x2**2 - 4*x1 - 6*x2'

    def execute(self):
        limitations = [ Limitation(limitation_str) for limitation_str in self.limitations ]
        point = Point( quadratic_simplex.simplex_method(fitness_function_str=str(self.fitness_function),
                                                     group_limitation=limitations
                                                     ) )

        self.algorithm_observer.point_observer.notify_all(Point.full_point(point, function_from_str(self.fitness_function)))
        print(Point.full_point(point, function_from_str(self.fitness_function)))


        func = function_from_str(self.fitness_function)
        result_info = f"Результат: точка ({point[0]:5f}, {point[1]:.5f}, {func(*point):.5f})"
        self.algorithm_observer.iteration_observer.notify_all(result_info)

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer