from PyQt6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox
from PyQt6 import uic
from src.entities.point import Point


class GeneticAlgorithmOptions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui/genetic_algorithm.ui', self)

    def get_point(self):
        return None

    def get_params(self):
        params = {}

        for widget in self.findChildren(QWidget):
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget_name = widget.objectName()
                if not widget_name:
                    continue

                params[widget_name] = float(widget.value())

        print(params)
        return params
