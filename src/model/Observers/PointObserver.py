from src.entities.Point import Point
from src.model.Observers.Observer import Observer

class PointObserver(Observer):
    def __init__(self):
        super().__init__()

    def notify_all(self, function, point: Point):
        [observer.get_point(function, point) for observer in self.observers]