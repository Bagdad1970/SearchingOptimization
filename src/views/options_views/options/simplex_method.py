from PyQt6.QtWidgets import QWidget, QLineEdit
from PyQt6 import uic

from src.entities.point import Point


class SimplexMethodOptions(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('src/views/options_views/ui/simplex_method.ui', self)

        self.add_limitations_btn.clicked.connect(self.add_limitation)
        self.delete_limitations_btn.clicked.connect(self.toggle_delete_mode)

        self.delete_limitations_btn.setCheckable(True)

        self.delete_mode = False

    def get_point(self, function):
        point = Point([0, 0])
        function_value = function(*point)
        point.append(function_value)
        return point

    def add_limitation(self):
        new_limitation = QLineEdit(self)
        new_limitation.setObjectName(f"limitation{self.limitations.count()}")

        new_limitation.mousePressEvent = lambda event, le=new_limitation: self.remove_limitation(event, le)

        self.limitations.addWidget(new_limitation)

    def toggle_delete_mode(self):
        self.delete_mode = self.delete_limitations_btn.isChecked()

        if not self.delete_mode:
            self.update_limitations_names()

    def remove_limitation(self, event, limitation):
        if self.delete_mode:
            self.limitations.removeWidget(limitation)
            limitation.deleteLater()
        else:
            QLineEdit.mousePressEvent(limitation, event)

    def update_limitations_names(self):
        for index in range(self.limitations.count()):
            widget = self.limitations.itemAt(index).widget()
            if isinstance(widget, QLineEdit):
                widget.setObjectName(f"limitation{index}")

    def get_params(self) -> dict:
        limitation_strings = []
        for index in range(self.limitations.count()):
            widget = self.limitations.itemAt(index).widget()
            if isinstance(widget, QLineEdit):
                limitation_strings.append(widget.text())

        return { 'limitations': limitation_strings }