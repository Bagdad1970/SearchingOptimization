class StrategyInterface:
    def set_params(self, function, **params):
        raise NotImplementedError

    def execute(self):
        raise NotImplementedError

    def set_algorithm_observer(self, algorithm_observer):
        raise NotImplementedError

    @classmethod
    def initial_function(cls) -> str:
        raise NotImplementedError