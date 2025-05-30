from PyQt6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit
from PyQt6 import uic
from src.entities.point import Point


class GeneticAlgorithmOptions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui/genetic_algorithm.ui', self)

    def get_point(self):
        return Point([0, 0, 0])

    def get_ranges(self) -> dict:
        params = {}
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QLineEdit):
                widget_name = widget.objectName()
                if not widget_name:
                    continue

                params[widget_name] = tuple(map(float,
                                                widget.text()
                                                .replace(')', '')
                                                .replace('(', '')
                                                .split(',')
                                                )
                                            )

        return params

    def get_params(self) -> dict:
        params = {}

        for widget in self.findChildren(QWidget):
            if isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                widget_name = widget.objectName()
                if not widget_name:
                    continue
                params[widget_name] = float(widget.value())

        return {**params, **self.get_ranges()}
