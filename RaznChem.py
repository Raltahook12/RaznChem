import sys

import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm

from PySide6 import QtCore, QtWidgets, QtGui,QtCharts,QtDataVisualization
from PySide6.QtWidgets import QApplication, QWidget,QComboBox,QSizePolicy,QHBoxLayout,QVBoxLayout,QPushButton
from PySide6.QtDataVisualization import Q3DSurface,QSurface3DSeries,QAbstract3DGraph
from PySide6.QtCore import Qt,QSize,QAbstractTableModel,QByteArray,QModelIndex


class Window(QWidget):
    def __init__(self, graph, parent=None):
        super().__init__(parent)
        self._graph = graph
        self._container = QWidget.createWindowContainer(self._graph, self,
                                                        Qt.Widget)
        screen_size = self._graph.screen().size()
        self._container.setMinimumSize(QSize(screen_size.width() / 2,
                                       screen_size.height() / 1.6))
        self._container.setMaximumSize(screen_size)
        self._container.setSizePolicy(QSizePolicy.Expanding,
                                      QSizePolicy.Expanding)
        self._container.setFocusPolicy(Qt.StrongFocus)

        h_layout = QHBoxLayout(self)
        v_layout = QVBoxLayout()
        h_layout.addWidget(self._container, 1)
        h_layout.addLayout(v_layout)
        v_layout.addWidget(QPushButton("Just button"))
        
if __name__ == "__main__":
    app = QApplication.instance()
    if app is None:    
        app = QApplication(sys.argv)
    graph = Q3DSurface()
    graph.addSeries([1,2,3])

    window = Window(graph)
    window.setWindowTitle("Surface example")
    window.show()

    sys.exit(app.exec())

# R = 0.015 # m
# D = 10**-6 # m2/s
# N = 200 # R steps Number
# total_time = 40 # s
#
# r = np.linspace(0, R, N + 1) # here N + 1 because otherwise the step will be wrong
# dr = R/N
# #print('r step size: ', dr)
# dt = 0.001 # если тут сделаешь из условия устойчивости расчет - будет круто
#
# #print('t step size: ', dt)
#
# N_time = int(total_time // dt) # integer division, int() is necessary
#
# t = np.linspace(0, dt * N_time, N_time + 1) # here N + 1 because otherwise the step will be wrong. "0" step is for initial conditions
#
# #print('U matrix size: ', N + 1, N_time + 1)
# u = np.zeros((N + 1, N_time + 1))
#
# u[0:-1, 0] = 1
# #print(u[:, 0])
# # main loop
# for tn in range(1, N_time+1):
#     #print(tn)
#     for j in range(1, N):
#         u[j, tn] = D * dt / dr**2 * (u[j + 1, tn - 1] - 2 * u[j, tn - 1] + u[j - 1, tn - 1]) + 2\
#                     * D * dt / r[j] / dr * (u[j, tn - 1] - u[j - 1, tn - 1]) + u[j, tn - 1]
#     #print(u[:, tn])
#
#     # boundary conditions
#     u[0, tn] = u[1, tn]
#     u[-1, tn] = 0
#
# y, x = np.meshgrid(t, r)
