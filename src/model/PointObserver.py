from src.entities.Point import Point

class PointObserver:
    def __init__(self):
        self.observers = []

    def add_point_observer(self, observer):
        self.observers.append(observer)

    def notify_about_new_point(self, function, point: Point):
        [observer.get_point_from_algorithm(function, point) for observer in self.observers]

    def notify_about_new_iteration(self, iteration_info):
        [observer.get_iteration(iteration_info) for observer in self.observers]

    def remove_point_observers(self):
        self.observers.clear()