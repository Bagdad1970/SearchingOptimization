from src.entities.Point import Point

class PointObserver:
    def __init__(self):
        self.observers = []

    def add_point_observer(self, observer):
        self.observers.append(observer)

    def notify_about_new_point(self, point: Point):
        for observer in self.observers:
            observer.get_point_from_algorithm(point)

    def remove_point_observers(self):
        self.observers.clear()