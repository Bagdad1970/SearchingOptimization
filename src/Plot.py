import numpy
import numpy as np
from PyQt6.QtGui import QColor
from pyqtgraph import mkColor
from pyqtgraph.opengl import GLViewWidget, GLSurfacePlotItem, GLScatterPlotItem, GLGridItem

from src.entities.Point import Point

class Plot(GLViewWidget):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.set_camera()

        self.grid = GLGridItem()
        self.setup_grid()

        self.scatter_plot = GLScatterPlotItem()
        self.addItem(self.scatter_plot)

        self.surface_plot = None

        self.current_point = None

    def set_background(self):
        self.setBackgroundColor(mkColor(0, 0, 0))

    def set_camera(self):
        self.setCameraPosition(distance=20, elevation=25, azimuth=45)

    def setup_grid(self, size=20, spacing=1):
        self.grid.setSize(size, size, size)
        self.grid.setSpacing(spacing, spacing, spacing)
        self.grid.setColor(mkColor(255, 255, 255))
        self.addItem(self.grid)

    def set_full_plot(self, function, point: Point):

        self.set_point(function=function, point=point)
        self.set_surface(function=function, point=point)

    def set_point(self, *, function, point: Point):
        """Обновляет точку на графике"""
        if self.current_point is not None:
            self.removeItem(self.current_point)  # Удаляем старую точку

        three_dimension_point = Point([point[0], point[1], function(*point)])
        self.current_point = GLScatterPlotItem(pos=np.array(three_dimension_point), color=(0, 0.5, 0, 1), size=20, pxMode=True)
        self.addItem(self.current_point)

    def set_surface(self, *, function, point: Point):
        x_grid_size, y_grid_size, z_grid_size = self.grid.size()
        x, y = point.create_points_array(x_length=x_grid_size, y_length=y_grid_size)
        X, Y = np.meshgrid(x, y)
        Z = function(X, Y)

        # Создание поверхности
        new_surface = GLSurfacePlotItem(x=x, y=y, z=Z)

        color = QColor(255, 39, 39, 255)
        new_surface.setColor(color)

        if self.surface_plot is not None:
            self.removeItem(self.surface_plot)

        self.surface_plot = new_surface
        self.addItem(self.surface_plot)