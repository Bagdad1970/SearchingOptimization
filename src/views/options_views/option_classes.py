from PyQt6.QtWidgets import QWidget
from PyQt6 import uic
from src.views.options import Options

class GradientDescentOptions(Options, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui_views/gradient_descent.ui', self)

class SimplexMethodOptions(Options, QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui_views/simplex_method.ui', self)