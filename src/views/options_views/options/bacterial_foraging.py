from collections.abc import Callable
from PyQt6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit
from PyQt6 import uic
from src.entities.point import Point
import src.views.options_views.options.option_utils as option_utils


class BacterialForagingOptions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui/bacterial_foraging.ui', self)

    def get_point(self, function: Callable):
        point = Point([0, 0, 0])
        return point

    def get_ranges(self) -> dict:
        params = {}
        for widget in self.findChildren(QWidget):
            if isinstance(widget, QLineEdit):
                widget_name = widget.objectName()

                if 'range' in widget_name:
                    params[widget_name] = tuple(map(float, option_utils.split_tuple_param(widget.text())))

        return params

    def get_max_min_values(self) -> dict:
        ranges_data = self.get_ranges()

        min_values = (ranges_data.get('x_range')[0], ranges_data.get('y_range')[0])
        max_values = (ranges_data.get('x_range')[1], ranges_data.get('y_range')[1])

        return { 'min_values': min_values, 'max_values': max_values }

    def get_numeric_params(self):
        params = {}
        for widget in self.findChildren(QWidget):
            if isinstance(widget, (QDoubleSpinBox, QSpinBox)):
                widget_name = widget.objectName()
                params[widget_name] = float(widget.value())

        return params

    def get_params(self) -> dict:
        return { **self.get_numeric_params(), **self.get_max_min_values() }
