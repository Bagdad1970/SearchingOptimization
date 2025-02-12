import pyqtgraph.opengl as gl

class Plot:
    def __init__(self):
        self.plot = gl.GLViewWidget()
        self.configure_plot()

    def configure_plot(self):
        self.plot.setBackgroundColor('k')
        self.plot.setCameraPosition(distance=80, elevation=60, azimuth=45)

        self.add_grid()

    def add_grid(self):
        # Добавление сетки
        grid = gl.GLGridItem()
        grid.setSize(20, 20)
        grid.setSpacing(1, 1)
        self.plot.addItem(grid)

