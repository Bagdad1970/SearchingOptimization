import numpy as np
from src.entities.point import Point
from src.model.strategies.strategy_interface import StrategyInterface
from collections.abc import Callable
from src.function_from_str import function_from_str


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
    ):
        self.function = function
        self.min_values = min_values
        self.max_values = max_values
        self.current_velocity_ratio = current_velocity_ratio
        self.local_velocity_ratio = local_velocity_ratio
        self.global_velocity_ratio = global_velocity_ratio
        self.position = self.particle_position()
        self.velocity = self.particle_velocity()
        self.best_position = self.position.copy()
        self.best_value = self.function(*self.position)

    def particle_position(self):
        return np.random.rand(2) * (self.max_values - self.min_values) + self.min_values

    def particle_velocity(self):
        return (
                np.random.rand(2) * (self.max_values - self.min_values)
                - (self.max_values - self.min_values) / 2
        )

    def compute_common_ratio(self) -> float:
        velo_ratio = self.local_velocity_ratio + self.global_velocity_ratio
        return 2.0 / abs(2.0 - velo_ratio - np.sqrt(velo_ratio ** 2 - 4.0 * velo_ratio))

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

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer

    def set_params(self, function, **params):
        self.function = function_from_str(function)
        self.initial_point = params.get("initial_point", Point([0, 0]))
        self.max_iterations = int(params.get("max_iterations", self.max_iterations))
        self.swarm_size = int(params.get("swarm_size", self.swarm_size))
        self.current_velocity_ratio = float(
            params.get("current_velocity_ratio", self.current_velocity_ratio)
        )
        self.local_velocity_ratio = float(
            params.get("local_velocity_ratio", self.local_velocity_ratio)
        )
        self.global_velocity_ratio = float(
            params.get("global_velocity_ratio", self.global_velocity_ratio)
        )
        self.min_values = np.array(params.get("min_values", self.min_values))
        self.max_values = np.array(params.get("max_values", self.max_values))
        self.stagnation_threshold = int(params.get("no_changes_iterations_count", self.stagnation_threshold))

    @staticmethod
    def initial_function() -> str:
        return "20 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))"

    @staticmethod
    def get_global_best_position(swarm: list, global_best_value):
        for particle in swarm:
            if particle.best_value == global_best_value:
                return particle.best_position.copy()
        return None

    @staticmethod
    def get_global_best_value(swarm: list):
        return min(particle.best_value for particle in swarm)

    def create_swarm(self):
        return [
            Particle(
                function=self.function,
                min_values=self.min_values,
                max_values=self.max_values,
                current_velocity_ratio=self.current_velocity_ratio,
                local_velocity_ratio=self.local_velocity_ratio,
                global_velocity_ratio=self.global_velocity_ratio,
            )
            for _ in range(self.swarm_size)
        ]

    def check_stagnation(self, current_best_value):
        if np.isclose(current_best_value, self.previous_best_value, atol=1e-10):
            self.stagnation_counter += 1
        else:
            self.stagnation_counter = 0
            self.previous_best_value = current_best_value

        return self.stagnation_counter >= self.stagnation_threshold

    def execute(self):
        self.swarm = self.create_swarm()
        self.global_best_value = self.get_global_best_value(self.swarm)
        self.global_best_position = self.get_global_best_position(
            self.swarm, self.global_best_value
        )
        self.previous_best_value = self.global_best_value

        for i in range(self.max_iterations):
            for particle in self.swarm:
                particle.update(self.global_best_position)
                if particle.best_value < self.global_best_value:
                    self.global_best_value = particle.best_value
                    self.global_best_position = particle.best_position.copy()

            if self.algorithm_observer:
                self.algorithm_observer.iteration_observer.notify_all(
                    f"Итерация {i+1}: F({self.global_best_position[0]:.5f}, {self.global_best_position[1]:.5f}) = {self.function(*self.global_best_position):.5f}"
                )

            if self.check_stagnation(self.global_best_value):
                if self.algorithm_observer:
                    self.algorithm_observer.iteration_observer.notify_all(
                        f"Алгоритм остановлен из-за стагнации на итерации {i+1}"
                    )
                    print(i)
                break

        if self.algorithm_observer:
            self.algorithm_observer.iteration_observer.notify_all(
                f"Результат: точка ({self.global_best_position[0]:.5f}, {self.global_best_position[1]:.5f}), значение: {self.function(*self.global_best_position):.5f}"
            )