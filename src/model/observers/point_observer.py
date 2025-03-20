from src.entities.point import Point
from src.model.observers.observer import Observer

class PointObserver(Observer):
    def __init__(self):
        super().__init__()

    def notify_all(self, point: Point):
        [observer.get_point(point) for observer in self.observers]

