from src.model.strategy_interface import StrategyInterface

class SimplexMethod(StrategyInterface):
    def __init__(self):
        super().__init__()

    def set_params(self, function, **params):
        pass

    def execute(self):
        pass

    def set_algorithm_observer(self, algorithm_observer):
        pass