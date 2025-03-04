import numpy as np
import pyqtgraph
from pyqtgraph.opengl import GLScatterPlotItem, GLGridItem

from src.entities.point import Point


class PlotPresenter:
    def __init__(self, *, view, model):
        self.view = view
        self.model = model

    def set_point(self, *, function, point: Point):

        self.view.set_point(point)

    def setup_grid(self, *, size=30, spacing=1):
        pass