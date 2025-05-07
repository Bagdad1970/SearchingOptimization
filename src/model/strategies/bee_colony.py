from collections.abc import Callable
import random

from src.function_from_str import function_from_str
from src.model.strategies.strategy_interface import StrategyInterface


class Bee:
    def __init__(self, *, function: Callable, min_values: list[float], max_values: list[float]):
        self.position = []
        self.function = function
        self.min_values = min_values
        self.max_values = max_values
        self.fitness = 0.0
        self.go_to_random_position()

    def calculate_fitness(self):
        self.fitness = -self.function(*self.position)

    def __lt__(self, other):
        return self.fitness < other.fitness

    def otherpatch(self, bee_list: list, range_list: tuple[float]) -> bool:
        if not bee_list:
            return True

        for bee in bee_list:
            bee_position = bee.get_position()
            if all(abs(self.position[i] - bee_position[i]) <= range_list[i]
                   for i in range(len(self.position))):
                return False
        return True

    def get_position(self) -> list[float]:
        return self.position.copy()

    def go_to(self, otherpos: list[float], range_list: list[float]):
        self.position = [
            otherpos[i] + random.uniform(-range_list[i], range_list[i])
            for i in range(len(otherpos))
        ]
        self.check_position()
        self.calculate_fitness()

    def go_to_random_position(self):
        self.position = [
            random.uniform(self.min_values[i], self.max_values[i])
            for i in range(len(self.min_values))
        ]
        self.check_position()
        self.calculate_fitness()

    def check_position(self):
        self.position = [
            max(self.min_values[i], min(self.max_values[i], self.position[i]))
            for i in range(len(self.position))
        ]


class BeeColony(StrategyInterface):
    def __init__(self):
        self.algorithm_observer = None
        self.function = None
        self.iterations = 100
        self.scout_bee_count = 50
        self.selected_bee_count = 10
        self.best_bee_count = 5
        self.selected_area_count = 5
        self.best_area_count = 3
        self.range_list = None
        self.min_values = None
        self.max_values = None

        self.bestposition = None
        self.bestfitness = -float('inf')
        self.best_areas = []
        self.selected_areas = []
        self.swarm = None

    def set_params(self, function: str, **params):
        self.function = function_from_str(function)
        self.iterations = int(params.get('iteration_count', self.iterations))
        self.scout_bee_count = int(params.get('scout_bee_count', self.scout_bee_count))
        self.selected_bee_count = int(params.get('selected_bee_count', self.selected_bee_count))
        self.best_bee_count = int(params.get('best_bee_count', self.best_bee_count))
        self.selected_area_count = int(params.get('selected_area_count', self.selected_area_count))
        self.best_area_count = int(params.get('best_area_count', self.best_area_count))

        self.range_list = params.get('range_list', self.best_area_count)

        self.min_values = params['min_values']
        self.max_values = params['max_values']

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer

    @staticmethod
    def initial_function() -> str:
        return "20 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))"

    def init_swarm(self):
        total_bee_count = (self.scout_bee_count +
                     self.selected_bee_count * self.selected_area_count +
                     self.best_bee_count * self.best_area_count)
        self.swarm = [Bee(function=self.function,
                          min_values=self.min_values,
                          max_values=self.max_values)
                      for _ in range(total_bee_count)]
        self.update_the_best()

    def update_the_best(self):
        """Update information about the best solution found"""
        self.swarm.sort(reverse=True)  # сортируем пчелок по убыванию значений целевой функции
        self.bestposition = self.swarm[0].get_position()  # берем позицию лучшей пчелки
        self.bestfitness = self.swarm[0].fitness  # берем значение целевой функции лучшей пчелки

    def send_bees(self, position: list[float], index: int, bee_count: int) -> int:
        for _ in range(bee_count):
            if index >= len(self.swarm):
                break
            if self.swarm[index] not in self.best_areas + self.selected_areas:  # если пчела еще не в лучших и перспективных областях,
                self.swarm[index].go_to(position, self.range_list)  # то отправим ее в окрестность некоторй позиции
            index += 1
        return index

    def next_step(self):
        self.best_areas = []
        self.selected_areas = []
        self.swarm.sort(reverse=True)

        for bee in self.swarm:
            if len(self.best_areas) < self.best_area_count and bee.otherpatch(self.best_areas, self.range_list):
                self.best_areas.append(bee)
            elif (len(self.selected_areas) < self.selected_area_count and
                  bee.otherpatch(self.best_areas + self.selected_areas, self.range_list)):
                self.selected_areas.append(bee)
            if len(self.best_areas) == self.best_area_count and len(self.selected_areas) == self.selected_area_count:
                break

        # Send bees to explore
        bee_index = 1

        for best_bee in self.best_areas:
            bee_index = self.send_bees(best_bee.get_position(), bee_index, self.best_bee_count)

        for selected_bee in self.selected_areas:
            bee_index = self.send_bees(selected_bee.get_position(), bee_index, self.selected_bee_count)

        # Remaining bees explore randomly
        for bee in self.swarm[ bee_index : ]:
            bee.go_to_random_position()

        self.update_the_best()

    def execute(self):
        self.init_swarm()

        for iteration in range(self.iterations):
            self.next_step()

            if self.algorithm_observer:
                self.algorithm_observer.iteration_observer.notify_all(
                    f"Итерация {iteration + 1}: F({self.bestposition[0]:.5f}, {self.bestposition[1]:.5f}) = {-self.bestfitness:.5f}"
                )

        if self.algorithm_observer:
            self.algorithm_observer.iteration_observer.notify_all(
                f"Результат: точка ({self.bestposition[0]:.5f}, {self.bestposition[1]:.5f}), значение: {-self.bestfitness:.5f}"
            )

        return self.bestposition, -self.bestfitness