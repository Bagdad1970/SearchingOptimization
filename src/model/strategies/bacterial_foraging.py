import time

import numpy as np

from src.function_from_str import function_from_str
from src.model.strategies.strategy_interface import StrategyInterface


class Bacterium:
    def __init__(self, bounds_lower, bounds_upper):
        self.bounds = [bounds_lower, bounds_upper]
        self.position = np.random.uniform(self.bounds[0], self.bounds[1], 2)
        self.health = 0.0
        self.direction = np.random.uniform(-1, 1, 2)
        self.direction = self.direction / np.linalg.norm(self.direction)

    def update_health(self, fitness):
        self.health += fitness


class BacterialForaging(StrategyInterface):

    def __init__(self):
        self.algorithm_observer = None
        self.function = None
        self.iteration_count = 100
        self.num_bacteria = 50
        self.chemotaxis_steps = 100
        self.reproduction_steps = 4
        self.elimination_steps = 2
        self.step_size = 0.1
        self.elimination_prob = 0.25
        self.elimination_count = 10
        self.bounds_lower = -5.12
        self.bounds_upper = 5.12
        self.stagnation_counter = 0  # Счетчик шагов без улучшений
        self.prev_best_fitness = float('inf')

        self.min_values = None
        self.max_values = None

        self.best_fitness = float('inf')
        self.best_position = None

        self.fitness_value_iters = []

        self.is_ok = True

    def set_params(self, function, **params):
        self.is_ok = True#params.get('is_ok')
        if self.is_ok:
            self.function = function_from_str(function)
            self.iteration_count = int(params.get('iteration_count', self.iteration_count))
            self.num_bacteria = int(params.get("num_bacteria", 50))
            self.chemotaxis_steps = int(params.get("chem_steps", 100))
            self.reproduction_steps = int(params.get("repro_steps", 4))

            self.elimination_steps = int(params.get("elim_steps", 2))
            self.step_size = float(params.get("step_size", 0.1))
            self.elimination_prob = float(params.get("elim_prob", 0.25))
            self.elimination_count = int(params.get("elim_count", 2))
            self.bounds_lower = float(params.get("bounds_lower", -5.12))
            self.bounds_upper = float(params.get("bounds_upper", 5.12))

            self.stagnation_threshold = int(params.get("no_changes_iterations_count", 10))

            self.is_ok = True


    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer


    @staticmethod
    def initial_function() -> str:
        return "20 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))"


    def create_initial_population(self):
        return [Bacterium(self.bounds_lower, self.bounds_upper)
                for _ in range(self.num_bacteria)]


    def chemotaxis(self, bacteria, step_size):
        for bacterium in bacteria:
            # Вычисляем текущую пригодность
            current_fitness = self.function(*bacterium.position)
            bacterium.update_health(current_fitness)

            # Вычисляем новую позицию по формуле (4.1)
            new_position = bacterium.position + step_size * bacterium.direction
            new_position = np.clip(new_position, self.bounds_lower, self.bounds_upper)
            new_fitness = self.function(*new_position)

            # Плавание
            if new_fitness < current_fitness:
                bacterium.position = new_position

                for _ in range(2):
                    # Двигаемся в ТОМ ЖЕ направлении (direction не меняется)
                    new_position = bacterium.position + step_size * bacterium.direction
                    new_position = np.clip(new_position, self.bounds_lower, self.bounds_upper)
                    new_fitness = self.function(*new_position)

                    if new_fitness >= self.function(*bacterium.position):
                        break

                    bacterium.position = new_position
            else:
                # Кувырок
                bacterium.direction = np.random.uniform(-1, 1, 2)
                bacterium.direction = bacterium.direction / np.linalg.norm(bacterium.direction)
                bacterium.position += step_size * bacterium.direction
                bacterium.position = np.clip(bacterium.position, self.bounds_lower, self.bounds_upper)

    def reproduction(self, bacteria):
        bacteria.sort(key=lambda b: b.health)
        survivors = bacteria[: self.num_bacteria // 2]
        new_bacteria = [Bacterium(self.bounds_lower, self.bounds_upper)
                        for _ in range(self.num_bacteria // 2)]

        # Клонирование лучших
        for i, survivor in enumerate(survivors):
            new_bacteria[i].position = survivor.position.copy()

        return survivors + new_bacteria

    def elimination_and_dispersal(self, bacteria):
        for i in np.random.choice(len(bacteria), self.elimination_count, replace=False):
            if np.random.random() < self.elimination_prob:
                bacteria[i] = Bacterium(self.bounds_lower, self.bounds_upper)
        return bacteria

    def update_best_solution(self, bacteria):
        current_best = min(bacteria, key=lambda b: self.function(*b.position))
        current_fitness = self.function(*current_best.position)

        if current_fitness < self.best_fitness:
            self.best_fitness = current_fitness
            self.best_position = current_best.position.copy()

    def check_stagnation(self):
        if np.isclose(self.best_fitness, self.prev_best_fitness, atol=1e-6):
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0
            self.prev_best_fitness = self.best_fitness

        return self.stagnation_counter >= self.stagnation_threshold

    def get_best_value(self):
        return self.best_fitness

    def get_execute_time(self):
        return self.execute_time

    def execute(self):
        if self.is_ok:
            time_start = time.time()

            bacteria_population = self.create_initial_population()

            for iteration in range(self.iteration_count):
                for elim_step in range(self.elimination_steps):
                    for repro_step in range(self.reproduction_steps):
                        for chem_step in range(self.chemotaxis_steps):
                            step_size = self.step_size / (chem_step + 1)
                            self.chemotaxis(bacteria_population, step_size)

                        bacteria_population = self.reproduction(bacteria_population)

                    bacteria_population = self.elimination_and_dispersal(bacteria_population)
                    self.update_best_solution(bacteria_population)

                print(self.best_fitness)

                if self.check_stagnation():
                    if self.algorithm_observer:
                        self.algorithm_observer.iteration_observer.notify_all(
                            f"Алгоритм остановлен из-за стагнации на итерации {iteration}"
                        )
                    break

                if self.algorithm_observer:
                    self.algorithm_observer.iteration_observer.notify_all(
                        f"Итерация {iteration + 1}: F({self.best_position[0]: .5f}, {self.best_position[1]: .5f}) = {self.best_fitness: .5f}"
                    )

            self.execute_time = time.time() - time_start
            print(self.execute_time)

            if self.algorithm_observer:
                self.algorithm_observer.iteration_observer.notify_all(
                    f"Результат: точка ({self.best_position[0]}, {self.best_position[1]}), значение: {self.best_fitness}"
                )