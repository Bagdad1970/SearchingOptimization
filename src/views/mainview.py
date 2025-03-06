from PyQt6.QtWidgets import QMainWindow

from src.plot_widget import PlotWidget
from src.views.view_interface import ViewInterface
from PyQt6 import uic  # Используем uic для загрузки UI

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/mainwindow.ui', self)  # Загружаем UI в QWidget

        self.presenter = None

    def set_plot(self, plot):
        self.Plot.addWidget(plot)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def execute(self):
        self.presenter.execute()

    def clean_iterations(self):
        self.Iterations.setPlainText("")

    def get_function(self):
        return self.Function.text()

    def add_iteration_info(self,iteration_info: str):
        self.Iterations.appendPlainText(iteration_info)

    def add_stop_reason(self, stop_reason: str):
        self.Iterations.appendPlainText(stop_reason)
