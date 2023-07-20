from PySide6.QtWidgets import QWidget,QHBoxLayout
import pyqtgraph as pq
import pyqtgraph.opengl as gl

class MplCanvas(QWidget):
    def __init__(self, proj=None):
        if proj is None:
            super(MplCanvas,self).__init__(parent=None)

            self.layout = QHBoxLayout()
            self.setLayout(self.layout)
            self.fig = pq.PlotWidget()
            self.lineplot = self.fig.plotItem
            self.lineplot.setLimits(xMin = -1,yMin = -1)

            self.layout.addWidget(self.fig)
        elif proj == '3d':
            super(MplCanvas,self).__init__(parent=None)

            self.layout = QHBoxLayout()
            self.fig = gl.GLViewWidget()
            self.surface = gl.GLSurfacePlotItem()

            self.setLayout(self.layout)
            self.layout.addWidget(self.fig)
            self.fig.addItem(self.surface)

            self.surface.setData([1,2,3],[1,2,3],np.array[[1,2,3],[1,2,3]])
    def plot(self, x, y, z=None):
        if z is None:
            self.lineplot.plot(x, y * 10 ** 5)
        else:
            self.surface.setData(x,y,z)
