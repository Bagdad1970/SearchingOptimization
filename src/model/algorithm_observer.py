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