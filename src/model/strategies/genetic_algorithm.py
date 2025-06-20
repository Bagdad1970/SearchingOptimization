import numpy as np
from src.entities.point import Point
from src.function_from_str import function_from_str
from src.model.observers.algorithm_observer import AlgorithmObserver
from src.model.strategies.strategy_interface import StrategyInterface


class GeneticAlgorithm(StrategyInterface):
    def __init__(self):
        self.algorithm_observer = None
        self.function = None
        self.population_size = 100
        self.generations = 100
        self.mutation_prob = 0.2
        self.mutation_range = 0.5
        self.selection_pressure = 1.5
        self.elite_count = 2
        self.x_range = (-float('inf'), float('inf'))
        self.y_range = (-float('inf'), float('inf'))

    def set_params(self, function, **params):
        self.function = function_from_str(function)
        self.population_size = int(params.get("population_size", self.population_size))
        self.generations = int(params.get("generations", self.generations))
        self.mutation_prob = params.get("mutation_prob", self.mutation_prob)
        self.mutation_range = params.get("mutation_range", self.mutation_range)
        self.selection_pressure = params.get("selection_pressure", self.selection_pressure)
        self.elite_count = int(params.get("elite_count", self.elite_count))
        self.x_range = params.get("x_range", self.x_range)
        self.y_range = params.get("y_range", self.y_range)

    def set_algorithm_observer(self, algorithm_observer: AlgorithmObserver):
        self.algorithm_observer = algorithm_observer

    @staticmethod
    def initial_function() -> str:
        return "(x**2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2"

    def create_individual(self) -> Point:
        """Создает случайную точку в заданном диапазоне"""
        x = np.random.uniform(*self.x_range)
        y = np.random.uniform(*self.y_range)
        return Point([x, y])

    def rank_selection(
        self, population: list[Point], scores: list[float], num_parents: int
    ) -> list[Point]:
        """Ранговый отбор для минимизации"""
        sorted_indices = np.argsort(scores)  # Сортировка от лучшего (минимального) к худшему (максимальному)
        ranks = np.arange(1, len(population) + 1) ** self.selection_pressure
        probability = ranks / np.sum(ranks)
        selected_indices = np.random.choice(
            sorted_indices, size=num_parents, p=probability
        )
        return [population[i] for i in selected_indices]

    @staticmethod
    def crossover(parent1: Point, parent2: Point) -> tuple[Point, Point]:
        """Арифметический кроссовер"""
        alpha = np.random.rand()
        child1 = parent1.scalar_multiply(alpha) + parent2.scalar_multiply(1 - alpha)
        child2 = parent2.scalar_multiply(alpha) + parent1.scalar_multiply(1 - alpha)
        return child1, child2

    def mutate(self, individual: Point) -> Point:
        """Мутация"""
        mutated = individual.copy()
        for i in range(len(mutated)):
            if np.random.rand() < self.mutation_prob:
                mutated[i] += np.random.uniform(-self.mutation_range, self.mutation_range)
                if i == 0:
                    mutated[i] = np.clip(mutated[i], *self.x_range)
                elif i == 1:
                    mutated[i] = np.clip(mutated[i], *self.y_range)
        return mutated

    def execute(self):
        """Запуск генетического алгоритма (минимизация target_function)"""
        population = [self.create_individual() for _ in range(self.population_size)]
        best_individual = None
        best_score = float('inf')

        for generation in range(self.generations):
            # Вычисление значений целевой функции
            scores = [self.function(*ind.get_point()) for ind in population]

            # Сохранение лучшего решения
            current_best_idx = np.argmin(scores)
            current_best_score = scores[current_best_idx]
            if current_best_score < best_score:
                best_score = current_best_score
                best_individual = population[current_best_idx].copy()

            self.algorithm_observer.iteration_observer.notify_all(
                f"Поколение {generation}: точка ({best_individual[0]:.5f}, {best_individual[1]:.5f}), "
                f"значение: {best_score:.5f}"
            )

            # Отбор родителей
            parents = self.rank_selection(
                population, scores, self.population_size // 2
            )

            # Скрещивание и мутация
            offspring = []
            for i in range(0, len(parents), 2):
                if i + 1 < len(parents):
                    child1, child2 = self.crossover(parents[i], parents[i + 1])
                    offspring.extend([self.mutate(child1), self.mutate(child2)])

            # Формирование новой популяции
            population = (
                    sorted(population, key=lambda x: self.function(*x.get_point()))[:self.elite_count]
                + offspring
            )
            population += [
                self.create_individual()
                for _ in range(self.population_size - len(population))
            ]

        self.algorithm_observer.point_observer.notify_all(
            Point.full_point(best_individual, self.function)
        )
        self.algorithm_observer.iteration_observer.notify_all(
            f"Результат: точка ({best_individual[0]:.5f}, {best_individual[1]:.5f}), "
            f"значение: {best_score:.5f}"
        )