class AlgorithmModel:
    def __init__(self, algorithm_strategy=None):
        self.algorithm_strategy = algorithm_strategy

    def set_algorithm(self, algorithm_strategy):
        self.algorithm_strategy = algorithm_strategy

    def get_graph(self):
        pass

    def execute_algorithm(self, params):
        pass

    def add_observer(self, observer):
        self.algorithm_strategy.add_observer(observer)
