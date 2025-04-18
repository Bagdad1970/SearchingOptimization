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

    def update(self, outer, global_best_position):
        random_local = np.random.rand(2)
        random_global = np.random.rand(2)
        velo_ratio = outer.local_velocity_ratio + outer.global_velocity_ratio
        common_ratio = (
            2.0
            * outer.current_velocity_ratio
            / abs(2.0 - velo_ratio - np.sqrt(velo_ratio**2 - 4.0 * velo_ratio))
        )

        new_velocity = (
            common_ratio * self.velocity
            + common_ratio
            * self.local_velocity_ratio
            * random_local
            * (self.best_position - self.position)
            + common_ratio
            * self.global_velocity_ratio
            * random_global
            * (global_best_position - self.position)
        )
        self.velocity = new_velocity
        self.position += self.velocity

        self.position = np.clip(self.position, self.min_values, self.max_values)

        value = self.function(self.position[0], self.position[1])
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
        self.min_values = [-5.12, -5.12]
        self.max_values = [5.12, 5.12]
        self.swarm = None
        self.global_best_position = None
        self.global_best_value = None

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
        self.min_values = params.get("min_values")
        self.max_values = params.get("max_values")

    @staticmethod
    def initial_function() -> str:
        return "20 + (x ** 2 - 10 * cos(2 * pi * x)) + (y ** 2 - 10 * cos(2 * pi * y))"

    @staticmethod
    def get_global_best_position(swarm: list, global_best_value):
        return next(
            particle.best_position
            for particle in swarm
            if particle.best_value == global_best_value
        )

    @staticmethod
    def get_global_best_value(swarm: list):
        return min(particle.best_value for particle in swarm)

    def create_swarm(self):
        swarm = [
            Particle(
                function=self.function,
                min_values=np.array(self.min_values),
                max_values=np.array(self.max_values),
                current_velocity_ratio=self.current_velocity_ratio,
                local_velocity_ratio=self.local_velocity_ratio,
                global_velocity_ratio=self.global_velocity_ratio,
            )
            for _ in range(self.swarm_size)
        ]
        return swarm

    def execute(self):
        if not self.swarm:
            self.swarm = self.create_swarm()
            self.global_best_value = self.get_global_best_value(self.swarm)
            self.global_best_position = self.get_global_best_position(
                self.swarm, self.global_best_value
            )

        for i in range(self.max_iterations):
            for particle in self.swarm:
                particle.update(self, self.global_best_position)
                if particle.best_value < self.global_best_value:
                    self.global_best_value = particle.best_value
                    self.global_best_position = particle.best_position.copy()

            self.algorithm_observer.iteration_observer.notify_all(
                f"Итерация {i}: f({self.global_best_position[0]:.5f}, {self.global_best_position[1]:.5f}) = {self.function(*self.global_best_position):.5f}"
            )

        self.algorithm_observer.iteration_observer.notify_all(
            f"Результат: точка ({self.global_best_position[0]:.5f}, {self.global_best_position[1]:.5f}), значение функции: {self.function(*self.global_best_position):.5f}"
        )
