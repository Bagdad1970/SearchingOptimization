from src.model.observers.observer import Observer

class IterationObserver(Observer):
    def __init__(self):
        super().__init__()

    def notify_all(self, iteration_info):
        [observer.get_iteration(iteration_info) for observer in self.observers]