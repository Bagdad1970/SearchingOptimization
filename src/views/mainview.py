from PyQt6.QtWidgets import QMainWindow

from src.plot_widget import PlotWidget
from src.views.view_interface import ViewInterface
from PyQt6 import uic  # Используем uic для загрузки UI

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/mainwindow.ui', self)  # Загружаем UI в QWidget

        #self.plot = PlotWidget()
        #self.set_plot()

        self.presenter = None

    def set_iteration_view(self, iteration_view):
        pass

    def set_plot(self):
        self.Plot.addWidget(self.plot)

    def set_presenter(self, presenter):
        self.presenter = presenter

    def set_plot(self):
        self.presenter.set_plot()

    def execute(self):
        self.presenter.execute()

    def clean_iterations(self):
        self.Iterations.setPlainText("")

    def get_function(self):
        return self.Function.text()