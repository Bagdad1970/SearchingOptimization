from PyQt6.QtWidgets import QApplication


class Observer:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observers(self):
        self.observers.clear()

    def update_events(self):
        [QApplication.processEvents() for observer in self.observers]