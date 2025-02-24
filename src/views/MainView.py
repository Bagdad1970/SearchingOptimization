from PyQt6.QtWidgets import QMainWindow
from src.views.ViewInterface import ViewInterface
from src.views.mainview import Ui_MainWindow

class MainView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.presenter = None

    def set_presenter(self, presenter):
        self.presenter = presenter

    def set_plot(self):
        self.presenter.set_plot()

    def execute(self):
        self.presenter.execute()

    def clean_iterations(self):
        self.ui.Iterations.setPlainText("")
