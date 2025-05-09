from src.model.observers.algorithm_observer import AlgorithmObserver
from src.model.strategies.strategy_interface import StrategyInterface


class Model:
    def __init__(self, *, strategy: StrategyInterface=None):
        self.strategy = strategy
        self.algorithm_observer = AlgorithmObserver()

    def set_strategy(self, strategy):
        self.strategy = strategy
        self.strategy.set_algorithm_observer(self.algorithm_observer)

    def set_params(self, function, params):
        self.strategy.set_params(function, **params)

    def execute(self):
        self.strategy.execute()

    def initial_function(self):
        return self.strategy.initial_function()

    def add_observer(self, key: str, observer):
        self.algorithm_observer.add_observer(key, observer)

    def remove_observers(self):
        self.algorithm_observer.remove_observers()