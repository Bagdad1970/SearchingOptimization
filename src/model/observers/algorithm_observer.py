from src.model.observers.iteration_observer import IterationObserver
from src.model.observers.point_observer import PointObserver
from src.model.observers.stop_reason_observer import StopReasonObserver


class AlgorithmObserver:
    def __init__(self):
        self.point_observer = PointObserver()
        self.iteration_observer = IterationObserver()
        self.stop_reason_observer = StopReasonObserver()

    def add_observer(self, key: str, observer):
        if key == 'point_observer':
            self.point_observer.add_observer(observer)
        elif key == 'stop_reason_observer':
            self.stop_reason_observer.add_observer(observer)
        elif key == 'iteration_observer':
            self.iteration_observer.add_observer(observer)
        else:
            raise TypeError("Invalid Observer class")

    def remove_observers(self):
        self.point_observer.remove_observers()
        self.stop_reason_observer.remove_observers()
        self.iteration_observer.remove_observers()