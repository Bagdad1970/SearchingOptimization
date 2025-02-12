from src.model.AlgorithmInterface import AlgorithmInterface

class AlgorithmModel:
    def __init__(self, strategy=None):
        self.strategy = strategy

    def set_algorithm(self, algorithm_strategy):
        self.strategy = algorithm_strategy

    def graph(self):
        return self.strategy.graph()

    def execute(self):
        solutions = self.strategy.execute()
        return solutions

    def add_observer(self, observer):
        self.strategy.add_observer(observer)
