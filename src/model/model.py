from src.model.algorithm_observer import AlgorithmObserver
from src.model.strategy_interface import StrategyInterface


class Model:
    def __init__(self, *, strategy: StrategyInterface=None):
        self.strategy = strategy
        self.algorithm_observer = AlgorithmObserver()

    def set_strategy(self, strategy):
        self.strategy = strategy
        self.strategy.set_algorithm_observer(self.algorithm_observer)

    def set_params(self, function, **params):
        self.strategy.set_params(function, **params)

    def execute(self):
        self.strategy.execute()

    def add_observer(self, key, observer):
        self.algorithm_observer.add_observer(key, observer)

    def remove_observers(self):
        self.algorithm_observer.remove_observers()