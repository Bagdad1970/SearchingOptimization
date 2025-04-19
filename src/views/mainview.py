from PyQt6.QtWidgets import QMainWindow
from src.views.view_interface import ViewInterface
from PyQt6 import uic

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/mainwindow.ui', self)

        self.presenter = None

        self.ExecuteButton.clicked.connect(self.execute)

    def set_plot(self, plot) -> None:
        self.Plot.addWidget(plot)

    def set_presenter(self, presenter) -> None:
        self.presenter = presenter

    def execute(self) -> None:
        self.presenter.execute()

    def clean_iterations(self) -> None:
        self.Iterations.setPlainText("")

    def get_function(self) -> str:
        return self.Function.text()

    def set_function(self, function: str) -> None:
        self.Function.setText(function)

    def add_iteration_info(self, iteration_info: str) -> None:
        self.Iterations.appendPlainText(iteration_info)

    def add_stop_reason(self, stop_reason: str) -> None:
        self.Iterations.appendPlainText(stop_reason)

    def get_x_limitation(self) -> tuple:
        return (abs(float(self.left_x.text())),
                abs(float(self.right_x.text()))
                )

    def get_y_limitation(self) -> tuple:
        return (abs(float(self.left_y.text())),
                abs(float(self.right_y.text()))
                )

    def get_area_lengths(self) -> dict:
        return {'x': self.get_y_limitation(),
                'y': self.get_y_limitation()
                }