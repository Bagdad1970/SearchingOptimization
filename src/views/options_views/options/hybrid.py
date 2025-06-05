from collections.abc import Callable
from PyQt6.QtWidgets import QWidget, QSpinBox, QDoubleSpinBox, QLineEdit, QMessageBox, QVBoxLayout
from PyQt6 import uic
from src.entities.point import Point
import src.views.options_views.options.option_utils as option_utils
from src.hybrid_plot import HybridPlot


class HybridBFO_PSOOptions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui/hybrid.ui', self)
        self.plot_dialog = None
        self.PlotsButton.clicked.connect(self.show_plots)

    def show_plots(self):
        if self.plot_dialog is None:
            self.plot_dialog = HybridPlot()
            self.plot_dialog.show()
        else:
            if self.plot_dialog.isHidden():
                self.plot_dialog = HybridPlot()  # Создаем новое окно, если было закрыто
                self.plot_dialog.show()
            else:
                self.plot_dialog.activateWindow()
                self.plot_dialog.raise_()


    def get_point(self, function: Callable):
        point = Point([0, 0, 0])
        for widget in self.findChildren(QWidget):
            if isinstance(widget, (QDoubleSpinBox, QSpinBox)):
                widget_name = widget.objectName()

                if widget_name == 'initial_point':
                    cleared_point = option_utils.split_tuple_param(widget.text())
                    point = Point(map(float, cleared_point))
                    function_value = function(*point)
                    point.append(function_value)

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

        is_ok = True
        if params.get('bfo_num_bacteria') % 2 != 0:
            QMessageBox.critical(None, "Ошибка", 'Число бактерий в популяции должно быть четно')
            is_ok = False

        return { **params, "is_ok" : is_ok }

    def get_params(self) -> dict:
        return { **self.get_numeric_params(), **self.get_max_min_values() }
