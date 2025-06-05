import random
import math
from typing import List, Tuple

from src.function_from_str import function_from_str
from src.model.strategies.strategy_interface import StrategyInterface


class Antibody:
    def __init__(self, position: List[float], fitness: float):
        self.position = position
        self.fitness = fitness


class ImmuneSystem(StrategyInterface):
    def __init__(
            self,
            num_best_antibodies: int = 5,
            num_clones: int = 10,
            selection_ratio: float = 0.2,
            ns: int = 3,
            death_ratio: float = 0.1,
            bc: float = 0.15,
            compression_ratio: float = 0.05,
            refresh_ratio: int = 3,
            bounds: Tuple[float, float] = (-5.0, 5.0)
    ):
        self.function = None
        self.algorithm_observer = None
        self.population_size = 50
        self.max_iterations = 100
        self.num_best_antibodies = num_best_antibodies
        self.num_clones = num_clones
        self.selection_ratio = selection_ratio
        self.ns = ns
        self.death_ratio = death_ratio
        self.bc = bc
        self.compression_ratio = compression_ratio
        self.refresh_ratio = refresh_ratio
        self.min_position, self.max_position = bounds

        self.antibodies = []
        self.memory_cells = []
        self.global_best_position = None
        self.global_best_fitness = float('inf')

    def set_params(self, function, **params):
        self.function = function_from_str(function)
        self.max_iterations = int(params.get("iteration_count", self.max_iterations))
        self.population_size = int(params.get("antibody_count", self.population_size))
        self.num_best_antibodies = int(params.get("num_best_antibodies", self.num_best_antibodies))
        self.num_clones = int(params.get("num_clones", self.num_clones))
        self.selection_ratio = float(params.get("selection_ratio", self.selection_ratio))
        self.death_ratio = float(params.get("death_ratio", self.death_ratio))
        self.compression_ratio = float(params.get("compression_ratio", self.compression_ratio))
        self.refresh_ratio = int(params.get("refresh_ratio", self.refresh_ratio))
        self.range_lower = params.get("range_lower", -5)
        self.range_upper = params.get("range_upper", 5)

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer

    @staticmethod
    def initial_function() -> str:
        return "x ** 2 + y ** 2"

    def initialize_population(self):
        for _ in range(self.population_size):
            position = [
                random.uniform(self.min_position, self.max_position),
                random.uniform(self.min_position, self.max_position)
            ]
            fitness = self.function(*position)
            self.antibodies.append(Antibody(position, fitness))

    def process_antigens(self):
        for antibody in self.antibodies:
            antibody.fitness = self.function(*antibody.position)

        sorted_antibodies = sorted(self.antibodies, key=lambda x: x.fitness)[:self.num_best_antibodies]

        clones = self.clone_and_mutate(sorted_antibodies)

        self.update_memory_cells(clones)

        surviving_clones = self.clonal_compression(clones)

        self.antibodies.extend(surviving_clones)

    def clone_and_mutate(self, antibodies: List[Antibody]) -> List[Antibody]:
        clones = []
        total_clones = self.num_best_antibodies * self.num_clones

        for antibody in antibodies:
            clone_count = max(1, int(round(self.num_clones / len(antibodies))))

            for _ in range(clone_count):
                cloned_position = antibody.position.copy()
                for j in range(len(cloned_position)):
                    cloned_position[j] += (random.random() * 2 - 1) * 0.5
                    cloned_position[j] = max(min(cloned_position[j], self.max_position), self.min_position)

                fitness = self.function(*cloned_position)
                clones.append(Antibody(cloned_position, fitness))

        # Корректировка числа клонов
        clones = clones[:total_clones]
        while len(clones) < total_clones and antibodies:
            antibody = random.choice(antibodies)
            cloned_position = antibody.position.copy()
            for j in range(len(cloned_position)):
                cloned_position[j] += (random.random() * 2 - 1) * 0.5
                cloned_position[j] = max(min(cloned_position[j], self.max_position), self.min_position)

            fitness = self.function(*cloned_position)
            clones.append(Antibody(cloned_position, fitness))

        return clones

    def update_memory_cells(self, clones: List[Antibody]):
        memory_selection_count = int(self.selection_ratio * self.num_best_antibodies * self.num_clones)
        clones_sorted = sorted(clones, key=lambda x: x.fitness)
        best_clones = clones_sorted[:memory_selection_count]
        self.memory_cells.extend(best_clones[:self.ns])
        self.memory_cells = [mc for mc in self.memory_cells if mc.fitness <= self.death_ratio]

    def clonal_compression(self, clones: List[Antibody]) -> List[Antibody]:
        surviving_clones = []
        for clone in clones:
            min_distance = float('inf')
            for other in [c for c in clones if c != clone]:
                distance = math.sqrt(
                    (clone.position[0] - other.position[0]) ** 2 +
                    (clone.position[1] - other.position[1]) ** 2
                )
                if distance < min_distance:
                    min_distance = distance

            bb_affinity = 1.0 / (1.0 + min_distance)
            if bb_affinity >= self.bc:
                surviving_clones.append(clone)

        return surviving_clones

    def prune_population(self):
        pruned_antibodies = []
        for antibody in self.antibodies:
            min_distance = float('inf')
            for other in [ab for ab in self.antibodies if ab != antibody]:
                distance = math.sqrt(
                    (antibody.position[0] - other.position[0]) ** 2 +
                    (antibody.position[1] - other.position[1]) ** 2
                )
                if distance < min_distance:
                    min_distance = distance

            bb_affinity = 1.0 / (1.0 + min_distance)
            if bb_affinity >= self.compression_ratio:
                pruned_antibodies.append(antibody)

        self.antibodies = pruned_antibodies

    def replace_worst_antibodies(self):
        self.antibodies = sorted(self.antibodies, key=lambda x: x.fitness)[:int(max(0, self.population_size - self.refresh_ratio))]

        for _ in range(self.refresh_ratio):
            position = [
                random.uniform(self.min_position, self.max_position),
                random.uniform(self.min_position, self.max_position)
            ]
            fitness = self.function(*position)
            self.antibodies.append(Antibody(position, fitness))

        if self.antibodies:
            current_best = min(self.antibodies, key=lambda x: x.fitness)
            if current_best.fitness < self.global_best_fitness:
                self.global_best_fitness = current_best.fitness
                self.global_best_position = current_best.position.copy()

    def execute(self):
        self.initialize_population()

        for iteration in range(self.max_iterations):
            self.process_antigens()
            self.prune_population()
            self.replace_worst_antibodies()

            if self.algorithm_observer:
                self.algorithm_observer.iteration_observer.notify_all(
                    f"Итерация {iteration + 1}: F({self.global_best_position[0]:.5f}, {self.global_best_position[1]:.5f}) = {self.global_best_fitness:.5f}"
                )

        if self.algorithm_observer:
            self.algorithm_observer.iteration_observer.notify_all(
                f"Результат: точка ({self.global_best_position[0]}, {self.global_best_position[1]}), значение: {self.global_best_fitness}"
            )