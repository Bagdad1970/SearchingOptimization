from src.model.Observers.IterationObserver import IterationObserver
from src.model.Observers.PointObserver import PointObserver
from src.model.Observers.StopReasonObserver import StopReasonObserver


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