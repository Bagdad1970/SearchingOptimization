from src.model.Observers.Observer import Observer

class StopReasonObserver(Observer):
    def __init__(self):
        super().__init__()

    def notify_all(self, stop_reason: str):
        [observer.get_stop_reason(stop_reason) for observer in self.observers]