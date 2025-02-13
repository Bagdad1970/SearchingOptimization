from src.views.options.gradient_descent import GradientDescentOptionsWidget
from PyQt6.QtWidgets import QWidget

class GradientDescentOptions(QWidget, GradientDescentOptionsWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)