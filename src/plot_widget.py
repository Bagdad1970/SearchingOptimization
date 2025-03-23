import numpy as np
import PyQt6.QtGui
import pyqtgraph
from pyqtgraph.opengl import GLViewWidget, GLSurfacePlotItem, GLScatterPlotItem, GLGridItem

from src.entities.point import Point

class PlotWidget(GLViewWidget):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.set_camera()

        self.grid = GLGridItem()
        self.set_grid()

        self.current_surface = None
        self.current_point = None

    def set_background(self):
        self.setBackgroundColor(pyqtgraph.mkColor(0, 0, 0))

    def set_camera(self):
        self.setCameraPosition(distance=20, elevation=25, azimuth=45)

    def remove_points(self):
        for widget in self.items:
            if isinstance(widget, GLScatterPlotItem):
                self.removeItem(widget)

        self.current_point = None

    def set_grid(self, *, size=30, spacing=1):
        self.grid.setSize(size, size)
        self.grid.setSpacing(spacing, spacing)
        self.grid.setColor(pyqtgraph.mkColor(255, 255, 255))
        self.addItem(self.grid)

    def set_point(self, point: Point):
        if self.current_point is not None:
            if self.current_point in self.items:
                self.removeItem(self.current_point)
            self.current_point = None

        point_plot = GLScatterPlotItem(
            pos=np.array([point]),
            color=(0, 0.5, 0, 1),
            size=20,
            pxMode=True
        )

        self.current_point = point_plot
        self.addItem(self.current_point)

    def set_plot(self, function, point: Point=None):
        if self.current_surface is not None:
            if self.current_surface in self.items:
                self.removeItem(self.current_surface)
            self.current_surface = None

        if point is not None:
            self.current_surface = self.surface_in_point(function, point)
            self.addItem(self.current_surface)
            #self.set_point(point)

    def surface_in_point(self, function, point: Point) -> GLSurfacePlotItem:
        x_grid_size, y_grid_size, z_grid_size = self.grid.size()
        x, y = point.create_points_array(x_length=x_grid_size, y_length=y_grid_size)
        X, Y = np.meshgrid(x, y)
        z = function(X, Y)

        surface = GLSurfacePlotItem(x=x, y=y, z=z)
        surface.setColor(PyQt6.QtGui.QColor(255, 39, 39, 255))

        return surface
