import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget


class PlotWidget(GLViewWidget):
    def __init__(self):
        super().__init__()
        self.set_background()
        self.set_camera()
        self.add_grid()

    def set_background(self):
        self.setBackgroundColor('k')

    def set_camera(self):
        self.setCameraPosition(distance=20, elevation=25, azimuth=45)

    def add_grid(self, size=20, spacing=1):
        grid = gl.GLGridItem()
        grid.setSize(size, size)
        grid.setSpacing(spacing, spacing)
        self.addItem(grid)

    def create_surface(self, *, x, y, function, **kwargs):
        X, Y = np.meshgrid(x, y)
        Z = function(X, Y)

        surface = gl.GLSurfacePlotItem(x=x, y=y, z=Z, shader='heightColor', smooth=True, **kwargs)
        surface.scale(x[1] - x[0], y[1] - y[0], 1)  # Масштабируем по осям

        self.addItem(surface)
