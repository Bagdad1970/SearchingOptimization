from src.model.observers.observer import Observer

class StopReasonObserver(Observer):
    def __init__(self):
        super().__init__()

    def notify_all(self, stop_reason: str):
        [observer.add_stop_reason(stop_reason) for observer in self.observers]
        self.update_events()