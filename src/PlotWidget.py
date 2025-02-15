import numpy
import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget, GLSurfacePlotItem


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

    def add_grid(self, size=20, spacing=2):
        grid = gl.GLGridItem()
        grid.setSize(size, size)
        grid.setSpacing(spacing, spacing)
        self.addItem(grid)

    def set_surface(self, params):
        x, y, function = params['x'], params['y'], params['function']
        X, Y = np.meshgrid(x, y) # поставить здесь Point
        Z = function(X, Y)

        surface = gl.GLSurfacePlotItem(x=x, y=y, z=Z, shader='heightColor', smooth=True)
        #old_surface = (item for item in self.items if isinstance(item, GLSurfacePlotItem))
        #print(type(old_surface))
        #if old_surface is not None:
        #    self.removeItem(old_surface)
        self.addItem(surface)
