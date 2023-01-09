import sys
import time

import numpy as np
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

import random

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        # a figure instance to plot on
        self.figure = plt.figure(figsize = [10,20])

        self.canvas = FigureCanvas(self.figure)

        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        # set the layout
        layout = QVBoxLayout()
        
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.button)
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)

    def plot(self):
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111,projection = '3d')

        R = 0.015 # m
        D = 10**-6 # m2/s
        N = 200 # R steps Number
        total_time = 40 # s
        
        r = np.linspace(0, R, N + 1) # here N + 1 because otherwise the step will be wrong
        dr = R/N
        #print('r step size: ', dr)
        dt = 0.001 # если тут сделаешь из условия устойчивости расчет - будет круто
        
        #print('t step size: ', dt)
        
        N_time = int(total_time // dt) # integer division, int() is necessary
        
        t = np.linspace(0, dt * N_time, N_time + 1) # here N + 1 because otherwise the step will be wrong. "0" step is for initial conditions
        
        #print('U matrix size: ', N + 1, N_time + 1)
        u = np.zeros((N + 1, N_time + 1))
        
        u[0:-1, 0] = 1
 
        #print(u[:, 0])
        # main loop
        for tn in range(1, N_time+1):
            #print(tn)
            for j in range(1, N):
                u[j, tn] = D * dt / dr**2 * (u[j + 1, tn - 1] - 2 * u[j, tn - 1] + u[j - 1, tn - 1]) + 2\
                            * D * dt / r[j] / dr * (u[j, tn - 1] - u[j - 1, tn - 1]) + u[j, tn - 1]
                            #print(u[:, tn])
                            
            # boundary conditions
            u[0, tn] = u[1, tn]
            u[-1, tn] = 0
            
            #append data to ploted array and redraw plot
        y,x = np.meshgrid(t,r)
        ax.plot_surface(x,y,u)
        
        # refresh canvas
        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main = Window()
    main.show()

    sys.exit(app.exec_())