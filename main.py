from PyQt6.QtWidgets import QApplication
import sys

from src.model.Model import Model
from src.presenter.Presenter import Presenter
from src.views.MainView import MainView


def main():
    app = QApplication(sys.argv)
    view = MainView()
    model = Model()
    presenter = Presenter(view=view, model=model)
    view.show()
    app.exec()

if __name__ == "__main__":
    main()