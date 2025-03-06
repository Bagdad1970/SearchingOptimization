from src.model.observers.iteration_observer import IterationObserver
from src.model.observers.point_observer import PointObserver
from src.model.observers.stop_reason_observer import StopReasonObserver


class AlgorithmObserver:
    def __init__(self):
        self._point_observer = PointObserver()
        self._iteration_observer = IterationObserver()
        self._stop_reason_observer = StopReasonObserver()

    @property
    def iteration_observer(self):
        return self._iteration_observer

    @property
    def point_observer(self):
        return self._point_observer

    @property
    def stop_reason_observer(self):
        return self._stop_reason_observer

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