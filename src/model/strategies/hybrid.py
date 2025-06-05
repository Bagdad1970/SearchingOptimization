import time

import numpy as np
from collections.abc import Callable
from src.entities.point import Point
from src.model.strategies.strategy_interface import StrategyInterface
from src.function_from_str import function_from_str


class Bacterium:
    def __init__(self, bounds_lower, bounds_upper, initial_position=None):
        self.bounds = [bounds_lower, bounds_upper]
        self.position = initial_position if initial_position is not None else np.random.uniform(self.bounds[0], self.bounds[1], 2)
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
        self.stagnation_counter = 0
        self.prev_best_fitness = float('inf')
        self.min_values = None
        self.max_values = None
        self.best_fitness = float('inf')
        self.best_position = None
        self.is_ok = True

        self.fitness_value_iters = []

    def set_params(self, function, **params):
        self.is_ok = params.get('is_ok', self.is_ok)
        if self.is_ok:
            self.function = function_from_str(function)
            self.iteration_count = int(params.get('bfo_iteration_count', self.iteration_count))
            self.num_bacteria = int(params.get("bfo_num_bacteria", 50))
            self.chemotaxis_steps = int(params.get("bfo_chemotaxsis_steps", 100))
            self.reproduction_steps = int(params.get("bfo_reproduction_steps", 4))
            self.elimination_steps = int(params.get("bfo_elimination_steps", 2))
            self.step_size = float(params.get("bfo_step_size", 0.1))
            self.elimination_prob = float(params.get("bfo_elimination_prob", 0.25))
            self.bounds_lower = float(params.get("bounds_lower", -5.12))
            self.bounds_upper = float(params.get("bounds_upper", 5.12))
            self.stagnation_threshold = int(params.get("no_changes_iterations_count", 10))
            self.min_values = np.array(params.get('min_values', [-5.12, -5.12]))
            self.max_values = np.array(params.get('max_values', [5.12, 5.12]))

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer

    @staticmethod
    def initial_function() -> str:
        return "20 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))"

    def create_initial_population(self, initial_positions=None):
        if initial_positions is None:
            return [Bacterium(self.bounds_lower, self.bounds_upper) for _ in range(self.num_bacteria)]
        else:
            initial_positions = initial_positions[:self.num_bacteria] + [None] * (self.num_bacteria - len(initial_positions))
            return [
                Bacterium(self.bounds_lower, self.bounds_upper, pos)
                for pos in initial_positions
            ]

    def chemotaxis(self, bacteria, step_size):
        for bacterium in bacteria:
            current_fitness = self.function(*bacterium.position)
            bacterium.update_health(current_fitness)
            new_position = bacterium.position + step_size * bacterium.direction
            new_position = np.clip(new_position, self.bounds_lower, self.bounds_upper)
            new_fitness = self.function(*new_position)
            if new_fitness < current_fitness:
                bacterium.position = new_position
                for _ in range(10):
                    new_position = bacterium.position + step_size * bacterium.direction
                    new_position = np.clip(new_position, self.bounds_lower, self.bounds_upper)
                    new_fitness = self.function(*new_position)
                    if new_fitness >= self.function(*bacterium.position):
                        break
                    bacterium.position = new_position
            else:
                bacterium.direction = np.random.uniform(-1, 1, 2)
                bacterium.direction = bacterium.direction / np.linalg.norm(bacterium.direction)
                bacterium.position += step_size * bacterium.direction
                bacterium.position = np.clip(bacterium.position, self.bounds_lower, self.bounds_upper)

    def reproduction(self, bacteria):
        bacteria.sort(key=lambda b: b.health)
        survivors = bacteria[:self.num_bacteria // 2]
        new_bacteria = [Bacterium(self.bounds_lower, self.bounds_upper) for _ in range(self.num_bacteria // 2)]
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

    def execute(self, initial_positions=None):
        if self.is_ok:
            bacteria_population = self.create_initial_population(initial_positions)
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

                message = f"Итерация {iteration + 1}: F({self.best_position[0]:6f}, {self.best_position[1]:6f}) = {self.best_fitness:6f}"
                if self.algorithm_observer:
                    self.algorithm_observer.iteration_observer.notify_all(message)

                if self.check_stagnation():
                    message = f"BFO остановлен из-за стагнации на итерации {iteration + 1}"
                    if self.algorithm_observer:
                        self.algorithm_observer.iteration_observer.notify_all(message)
                    break

            positions = [ bacterium.position.copy()  for bacterium in bacteria_population]
            return positions, self.best_position, self.best_fitness


class Particle:
    def __init__(
            self,
            *,
            function: Callable,
            min_values: np.ndarray,
            max_values: np.ndarray,
            current_velocity_ratio: float,
            local_velocity_ratio: float,
            global_velocity_ratio: float,
            initial_position: np.ndarray = None
    ):
        self.function = function
        self.min_values = min_values
        self.max_values = max_values
        self.current_velocity_ratio = current_velocity_ratio
        self.local_velocity_ratio = local_velocity_ratio
        self.global_velocity_ratio = global_velocity_ratio
        self.position = initial_position if initial_position is not None else self.particle_position()
        self.velocity = self.particle_velocity()
        self.best_position = self.position.copy()
        self.best_value = self.function(*self.position)

    def particle_position(self):
        return np.random.rand(2) * (self.max_values - self.min_values) + self.min_values

    def particle_velocity(self):
        return np.random.rand(2) * (self.max_values - self.min_values) + self.min_values

    def compute_common_ratio(self) -> float:
        velo_ratio = self.local_velocity_ratio + self.global_velocity_ratio
        return 2.0 * np.random.rand(1) / abs(2.0 - velo_ratio - np.sqrt(velo_ratio ** 2 - 4.0 * velo_ratio))

    def compute_new_velocity(self, common_ratio: float, global_best_position: np.ndarray):
        random_local = np.random.rand(2)
        random_global = np.random.rand(2)
        return common_ratio * (
                self.current_velocity_ratio * self.velocity
                + self.local_velocity_ratio * random_local * (self.best_position - self.position)
                + self.global_velocity_ratio * random_global * (global_best_position - self.position)
        )

    def update(self, global_best_position: np.ndarray):
        common_ratio = self.compute_common_ratio()
        self.velocity = self.compute_new_velocity(common_ratio, global_best_position)
        self.position += self.velocity
        self.position = np.clip(self.position, self.min_values, self.max_values)
        value = self.function(*self.position)
        if value < self.best_value:
            self.best_value = value
            self.best_position = self.position.copy()


class ParticleSwarm(StrategyInterface):
    def __init__(self):
        self.algorithm_observer = None
        self.function = None
        self.initial_point = None
        self.max_iterations = 100
        self.swarm_size = 50
        self.current_velocity_ratio = 0.5
        self.local_velocity_ratio = 2.0
        self.global_velocity_ratio = 2.0
        self.min_values = np.array([-5.12, -5.12])
        self.max_values = np.array([5.12, 5.12])
        self.swarm = None
        self.global_best_position = None
        self.global_best_value = float('inf')
        self.stagnation_threshold = 50
        self.stagnation_counter = 0
        self.previous_best_value = float('inf')
        self.fitness_value_iters = []

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer

    def set_params(self, function, **params):
        self.function = function_from_str(function)
        self.initial_point = params.get("pso_initial_point", Point([0, 0]))
        self.max_iterations = int(params.get("pso_iteration_count", self.max_iterations))
        self.swarm_size = int(params.get("pso_swarm_size", self.swarm_size))
        self.current_velocity_ratio = float(params.get("pso_current_velocity_ratio", self.current_velocity_ratio))
        self.local_velocity_ratio = float(params.get("pso_local_velocity_ratio", self.local_velocity_ratio))
        self.global_velocity_ratio = float(params.get("pso_global_velocity_ratio", self.global_velocity_ratio))
        self.min_values = np.array(params.get("min_values", self.min_values))
        self.max_values = np.array(params.get("max_values", self.max_values))
        self.stagnation_threshold = int(params.get("no_changes_iterations_count", self.stagnation_threshold))

    def create_swarm(self, initial_positions=None):
        if initial_positions is None:
            initial_positions = [None] * self.swarm_size
        else:
            initial_positions = initial_positions[:self.swarm_size] + [None] * (self.swarm_size - len(initial_positions))

        return [
            Particle(
                function=self.function,
                min_values=self.min_values,
                max_values=self.max_values,
                current_velocity_ratio=self.current_velocity_ratio,
                local_velocity_ratio=self.local_velocity_ratio,
                global_velocity_ratio=self.global_velocity_ratio,
                initial_position=pos
            )
            for pos in initial_positions
        ]

    def get_global_best_value(self):
        return min(particle.best_value for particle in self.swarm)

    def get_global_best_position(self, global_best_value):
        for particle in self.swarm:
            if particle.best_value == global_best_value:
                return particle.best_position.copy()
        return None

    def check_stagnation(self, current_best_value):
        if np.isclose(current_best_value, self.previous_best_value, atol=1e-10):
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0
            self.previous_best_value = current_best_value
        return self.stagnation_counter >= self.stagnation_threshold

    def execute(self, initial_positions=None):
        self.swarm = self.create_swarm(initial_positions)
        self.global_best_value = self.get_global_best_value()
        self.global_best_position = self.get_global_best_position(self.global_best_value)
        self.previous_best_value = self.global_best_value

        for iteration in range(self.max_iterations):
            for particle in self.swarm:
                particle.update(self.global_best_position)
                if particle.best_value < self.global_best_value:
                    self.global_best_value = particle.best_value
                    self.global_best_position = particle.best_position.copy()

            print(self.global_best_value)

            if self.algorithm_observer:
                self.algorithm_observer.iteration_observer.notify_all(
                    f"Итерация {iteration + 1}: F({self.global_best_position[0]:6f}, {self.global_best_position[1]}:6f) = {self.global_best_value:6f}"
                )

            if self.check_stagnation(self.global_best_value):
                message = f"PSO остановлен из-за стагнации на итерации {iteration+1}"
                if self.algorithm_observer:
                    self.algorithm_observer.iteration_observer.notify_all(message)
                break

        return self.global_best_position, self.global_best_value


class HybridBFO_PSO(StrategyInterface):
    def __init__(self):
        self.bfo = BacterialForaging()
        self.pso = ParticleSwarm()
        self.best_position = None
        self.best_value = float('inf')
        self.execute_time = None

    def get_best_value(self):
        return self.best_value

    def set_algorithm_observer(self, observer):
        self.bfo.set_algorithm_observer(observer)
        self.pso.set_algorithm_observer(observer)

    @staticmethod
    def initial_function() -> str:
        return "20 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))"

    def set_params(self, function: str, **params):
        self.bfo.set_params(function, **params)
        self.pso.set_params(function, **params)

    def get_execute_time(self):
        return self.execute_time

    def execute(self):
        time_start = time.time()

        if self.bfo.algorithm_observer:
            self.bfo.algorithm_observer.iteration_observer.notify_all(
                "Бактериальная оптимизация"
            )

        bfo_positions, bfo_best_position, bfo_best_value = self.bfo.execute()
        self.best_position = bfo_best_position
        self.best_value = bfo_best_value

        bfo_positions = sorted(bfo_positions, key=lambda pos: self.bfo.function(*pos))

        if self.bfo.algorithm_observer:
            self.bfo.algorithm_observer.iteration_observer.notify_all(
                f"BFO. Лучший результат: F({bfo_best_position[0]}, {bfo_best_position[1]}) = {bfo_best_value}"
            )

        if self.bfo.algorithm_observer:
            self.pso.algorithm_observer.iteration_observer.notify_all(
                "Рой частиц"
            )

        pso_best_position, pso_best_value = self.pso.execute(initial_positions=bfo_positions)

        if pso_best_value < self.best_value:
            self.best_position = pso_best_position
            self.best_value = pso_best_value

        if self.pso.algorithm_observer:
            self.pso.algorithm_observer.iteration_observer.notify_all(
                f"PSO. Лучший результат: F({pso_best_position[0]}, {pso_best_position[1]}) = {pso_best_value}"
            )
            self.pso.algorithm_observer.iteration_observer.notify_all(
                f"Итоговый лучший результат: F({self.best_position[0]}, {self.best_position[1]}) = {self.best_value}"
            )

        self.execute_time = time.time() - time_start
        if self.pso.algorithm_observer:
            self.pso.algorithm_observer.iteration_observer.notify_all(
                f"Время выполнения: {self.execute_time}"
            )

        return self.best_position, self.best_value