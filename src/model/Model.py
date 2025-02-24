class Model:
    def __init__(self, *, strategy=None):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def set_params(self, function, **params):
        self.strategy.set_params(function, **params)

    def get_initial_surface_params(self):
        return self.strategy.get_initial_surface_params()

    def execute(self):
        solutions = self.strategy.execute()
        return solutions

    def add_observer(self, point_observer):
        self.strategy.add_observer(point_observer)

    def remove_point_observers(self):
        if self.strategy is not None:
            self.strategy.remove_observers()