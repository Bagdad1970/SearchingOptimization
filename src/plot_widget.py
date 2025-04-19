import numpy as np
from PyQt6.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from src.entities.point import Point
from collections.abc import Callable


class Matplotlib3DWidget(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(8, 6))
        super().__init__(self.fig)
        self.setParent(parent)

        self.ax = self.fig.add_subplot(111, projection='3d')
        self.current_surface = None
        self.current_point = None
        self.set_camera()

    def set_camera(self, elev=30, azim=45):
        self.ax.view_init(elev=elev, azim=azim)
        self.ax.dist = 1

    def clear_plot(self):
        self.ax.clear()
        self.current_surface = None
        self.current_point = None
        self.set_camera()
        self.draw()

    def remove_points(self):
        if self.current_point is not None:
            try:
                self.current_point.remove()
            except (ValueError, AttributeError):
                pass
            self.current_point = None
        self.draw()

    def set_point(self, point: Point):
        self.remove_points()

        if point is not None:
            self.current_point = self.ax.scatter(
                [point[0]], [point[1]], [point[2]],
                color='green', s=100
            )
        self.draw()

    def set_plot(self, *, function, area: dict, point: Point = None):
        if self.current_surface is not None:
            try:
                self.current_surface.remove()
            except (ValueError, AttributeError):
                pass
            self.current_surface = None

        if point is not None:
            self.set_point(point)
        else:
            self.remove_points()

        self.current_surface = self.surface_in_point(
            function=function,
            point=point,
            area=area)

        print(function)
        print(point)
        print(area)

        self.draw()
        print('plot_draw')

    def surface_in_point(self, *, function: Callable, point: Point, area: dict):
        x = np.linspace(
            float(point[0] - area.get('x')[0]),
            float(point[0] + area.get('x')[1]),
            50
        )
        y = np.linspace(
            float(point[1] - area.get('y')[0]),
            float(point[1] + area.get('y')[1]),
            50
        )
        X, Y = np.meshgrid(x, y)
        Z = function(X, Y)

        surface = self.ax.plot_surface(
            X, Y, Z,
            cmap='viridis',
            alpha=0.8
        )
        return surface


class PlotWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.plot = Matplotlib3DWidget(self)
        self.layout.addWidget(self.plot)

    def set_point(self, point: Point):
        self.plot.set_point(point)

    def set_plot(self, function: Callable, area: dict, point: Point = None):
        self.plot.set_plot(
            function=function,
            area=area,
            point=point
        )

    def remove_points(self):
        self.plot.remove_points()

    def clear_plot(self):
        self.plot.clear_plot()