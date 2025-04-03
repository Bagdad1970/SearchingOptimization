class StrategyInterface:
    def set_params(self, function, **params):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def set_algorithm_observer(self, algorithm_observer):
        raise NotImplementedError

    @staticmethod
    def initial_function() -> str:
        raise NotImplementedError