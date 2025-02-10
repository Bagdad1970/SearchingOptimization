class Observer:
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def notify_all(self):
        for observer in self.observers:
            observer.get_notice()