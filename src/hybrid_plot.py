import os
import pickle
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QComboBox, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # Исправлен импорт
from matplotlib.figure import Figure


class HybridPlot(QWidget):
    def __init__(self, data_dir="hybrid_plots", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Просмотр графиков оптимизации")
        self.setGeometry(300, 300, 1000, 700)

        self.data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), data_dir)
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir, exist_ok=True)

        self.graph_files = {
            'Время и Итерации': 'time_iters.pickle',
            'Время и Размер популяции': 'time_pops.pickle',
            'Значения и Итерации': 'value_iters.pickle',
            'Значения и Размер популяции': 'value_pops.pickle'
        }

        self.init_ui()
        self.load_initial_graph()  # Загружаем первый график при инициализации

    def init_ui(self):
        layout = QVBoxLayout()

        self.combobox = QComboBox()
        for name, filename in self.graph_files.items():
            filepath = os.path.join(self.data_dir, filename)
            if os.path.exists(filepath):
                self.combobox.addItem(name)
        if self.combobox.count() == 0:
            self.combobox.addItem("Нет доступных графиков")
            self.combobox.setEnabled(False)
        else:
            self.combobox.setEnabled(True)
        self.combobox.currentTextChanged.connect(self.load_selected_graph)
        layout.addWidget(self.combobox)

        self.figure = Figure(figsize=(10, 6))
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

    def load_initial_graph(self):
        if self.combobox.count() > 0 and self.combobox.isEnabled():
            self.load_selected_graph(self.combobox.currentText())

    def load_selected_graph(self, graph_name):
        if not graph_name or graph_name not in self.graph_files:
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'График не выбран или не найден',
                    ha='center', va='center', fontsize=12)
            self.canvas.draw()
            return

        filepath = os.path.join(self.data_dir, self.graph_files.get(graph_name, ""))

        if not os.path.exists(filepath):
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, f'Файл {graph_name} не найден',
                    ha='center', va='center', fontsize=12)
            self.canvas.draw()
            return

        try:
            with open(filepath, 'rb') as f:
                fig = pickle.load(f)
                self.display_figure(fig)
        except Exception as e:
            print(f"Ошибка загрузки: {e}")
            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'Ошибка загрузки графика',
                    ha='center', va='center', fontsize=12, color='red')
            self.canvas.draw()

    def display_figure(self, fig):
        self.figure.clear()

        new_ax = self.figure.add_subplot(111)

        # Проверяем, является ли fig объектом Figure
        if isinstance(fig, Figure):
            for ax in fig.axes:
                for line in ax.lines:
                    new_ax.plot(
                        line.get_xdata(),
                        line.get_ydata(),
                        color=line.get_color(),
                        linestyle=line.get_linestyle(),
                        marker=line.get_marker(),
                        label=line.get_label()
                    )
                new_ax.set_title(ax.get_title())
                new_ax.set_xlabel(ax.get_xlabel())
                new_ax.set_ylabel(ax.get_ylabel())
                if ax.get_legend():
                    new_ax.legend()
                new_ax.grid(True)
        elif isinstance(fig, dict):
            x = fig.get('x', [])
            y = fig.get('y', [])
            if x and y:
                new_ax.plot(
                    x, y,
                    color=fig.get('color', 'blue'),
                    linestyle=fig.get('linestyle', '-'),
                    marker=fig.get('marker', None),
                    label=fig.get('label', None)
                )
                new_ax.set_title(fig.get('title', ''))
                new_ax.set_xlabel(fig.get('xlabel', ''))
                new_ax.set_ylabel(fig.get('ylabel', ''))
                if fig.get('label'):
                    new_ax.legend()
                new_ax.grid(True)
        else:
            new_ax.text(0.5, 0.5, 'Неподдерживаемый формат данных',
                        ha='center', va='center', fontsize=12, color='red')

        self.canvas.draw()