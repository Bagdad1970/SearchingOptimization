import numpy as np
import PyQt6.QtGui
import pyqtgraph
from pyqtgraph.opengl import GLViewWidget, GLSurfacePlotItem, GLScatterPlotItem, GLGridItem

from src.entities.Point import Point

class Plot(GLViewWidget):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.set_camera()

        self.grid = None
        self.setup_grid()

        self.surface_plot = None
        self.current_point = None

    def set_background(self):
        self.setBackgroundColor(pyqtgraph.mkColor(0, 0, 0))

    def set_camera(self):
        self.setCameraPosition(distance=20, elevation=25, azimuth=45)

    def setup_grid(self, size=30, spacing=1):
        self.grid = GLGridItem()
        self.grid.setSize(size, size)
        self.grid.setSpacing(spacing, spacing)
        self.grid.setColor(pyqtgraph.mkColor(255, 255, 255))
        self.addItem(self.grid)

    def set_full_plot(self, function, point: Point):
        self.set_surface(function=function, point=point)

    def set_point(self, *, function, point: Point):
        if self.current_point is not None:
            self.removeItem(self.current_point)

        # Получаем координаты точки
        three_dimension_point = [point[0], point[1], function(*point)]
        three_dimension_array = np.array([three_dimension_point])  # Преобразуем в [[x, y, z]]

        self.current_point = GLScatterPlotItem(
            pos=three_dimension_array,
            color=(0, 0.5, 0, 1),
            size=20,
            pxMode=True
        )
        self.addItem(self.current_point)

    def set_surface(self, *, function, point: Point):
        if self.surface_plot is not None:
            self.removeItem(self.surface_plot)

        x_grid_size, y_grid_size, z_grid_size = self.grid.size()
        x, y = point.create_points_array(x_length=x_grid_size, y_length=y_grid_size)
        X, Y = np.meshgrid(x, y)
        Z = function(X, Y)

        new_surface = GLSurfacePlotItem(x=x, y=y, z=Z)
        new_surface.setColor(PyQt6.QtGui.QColor(255, 39, 39, 255))

        self.surface_plot = new_surface
        self.addItem(self.surface_plot)
