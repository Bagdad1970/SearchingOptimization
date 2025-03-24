from src.model.observers.observer import Observer

class IterationObserver(Observer):
    def __init__(self):
        super().__init__()

    def notify_all(self, iteration_info: str):
        [observer.add_iteration_info(iteration_info) for observer in self.observers]
        self.update_events()