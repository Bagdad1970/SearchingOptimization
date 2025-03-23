import numpy as np

from src.model.strategy_interface import StrategyInterface


class GeneticAlgorithm(StrategyInterface):
    def __init__(self):
        self.algorithm_observer = None
        self.fitness_function = None
        self.population_size = 300
        self.genes = 2
        self.mutation_rate = 0.2
        self.elite_size = 5
        self.generations = 100
        self.population = None

    def set_algorithm_observer(self, algorithm_observer):
        self.algorithm_observer = algorithm_observer

    def set_params(self, function, **params):
        self.fitness_function = function
        self.population_size = params.get('population_size', self.population_size)
        self.genes = params.get('genes', self.genes)
        self.mutation_rate = params.get('mutation_rate', self.mutation_rate)
        self.elite_size = params.get('elite_size', self.elite_size)
        self.generations = params.get('generations', self.generations)
        self.population = None

    @staticmethod
    def initial_function() -> str:
        return '(1 - x)**2 + 100*(y-x**2)**2'

    def __create_population(self):
        return np.random.uniform(-2, 2, (self.population_size, self.genes))

    def __roulette_wheel_selection(self, scores):
        fitness_sum = np.sum(scores - np.min(scores) + 1e-6)
        selection_probs = (scores - np.min(scores) + 1e-6) / fitness_sum
        return self.population[np.random.choice(len(self.population), p=selection_probs)]

    @staticmethod
    def __crossover(parent1, parent2):
        alpha = np.random.uniform(0, 1)
        child1 = alpha * parent1 + (1 - alpha) * parent2
        child2 = alpha * parent2 + (1 - alpha) * parent1
        return child1, child2

    def __adaptive_mutation(self, individual, generation):
        adaptive_rate = self.mutation_rate * (1 - generation / self.generations)
        for i in range(self.genes):
            if np.random.rand() < adaptive_rate:
                individual[i] += np.random.uniform(-0.1, 0.1)
        return individual

    def execute(self):
        self.population = self.__create_population()

        for generation in range(self.generations):
            scores = np.array([self.fitness_function(ind) for ind in self.population])
            elite_indices = scores.argsort()[-self.elite_size:]
            new_population = self.population[elite_indices].tolist()

            while len(new_population) < self.population_size:
                parent1 = self.__roulette_wheel_selection(scores)
                parent2 = self.__roulette_wheel_selection(scores)
                child1, child2 = self.__crossover(parent1, parent2)
                new_population.append(self.__adaptive_mutation(child1, generation))
                if len(new_population) < self.population_size:
                    new_population.append(self.__adaptive_mutation(child2, generation))

            self.population = np.array(new_population)
            print(f"Поколение {generation}: Минимум = {-max(scores)}")

        best_index = np.argmax([self.fitness_function(ind) for ind in self.population])
        return self.population[best_index]


def rosenbrock(x):
    return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2

def fitness(individual):
    return -rosenbrock(individual)