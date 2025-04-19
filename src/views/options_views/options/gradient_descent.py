from PyQt6.QtWidgets import QWidget, QLineEdit, QSpinBox, QDoubleSpinBox
from PyQt6 import uic
from src.entities.point import Point


class GradientDescentOptions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui/gradient_descent.ui', self)

    def get_point(self, function) -> Point:
        point = Point([0, 0])
        for widget in self.findChildren(QWidget):
            widget_name = widget.objectName()
            if widget_name == 'PointCoord1':
                point[0] = float(widget.text())
            elif widget_name == 'PointCoord2':
                point[1] = float(widget.text())

        function_value = function(*point)
        point.append(function_value)

        return point

    def get_method_params(self) -> dict:
        method_params = {}
        classes_widgets_for_params = (QLineEdit, QSpinBox, QDoubleSpinBox)

        for widget in self.findChildren(QWidget):
            if isinstance(widget, classes_widgets_for_params):
                widget_name = widget.objectName()
                if not widget_name:
                    continue

                value = None
                if isinstance(widget, QLineEdit):
                    value = float(widget.text()) if widget.text() else 0.0
                elif isinstance(widget, (QSpinBox, QDoubleSpinBox)):
                    value = float(widget.value())

                method_params[widget_name] = value

        return method_params

    def get_params(self) -> dict:
        return {'point': self.get_point(), **self.get_method_params()}