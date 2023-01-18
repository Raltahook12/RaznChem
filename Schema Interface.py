import sys

import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout,QHBoxLayout,\
                            QLabel,QLineEdit,QGroupBox,QFormLayout,QMessageBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QLocale
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setMinimumSize(1200,800)
        # a figure instance to plot on
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        #LineEdit to set radius by user
        self.set_radius = QLineEdit()
        self.set_radius.setPlaceholderText('Input Radius')
        self.radiusValidator = QDoubleValidator()
        self.englishLocale = QLocale(QLocale.English)
        self.radiusValidator.setLocale(self.englishLocale)
        self.set_radius.setValidator(self.radiusValidator)

        #LineEdit to set diffusion coefficient
        self.set_diffuse = QLineEdit()
        self.set_diffuse.setPlaceholderText('Input Diffusion Coefficient')
        self.coefdiffValidator = QDoubleValidator()
        self.coefdiffValidator.Notation = QDoubleValidator.ScientificNotation
        self.set_diffuse.setLocale(self.englishLocale)
        self.set_diffuse.setValidator(self.coefdiffValidator)

        #button for plot
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        #set the layouts
        self.layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.general_statment = QGroupBox(title='General Statment')
        self.generalStatments_layout = QFormLayout()

        #add Widgets to layouts
        #main layout
        self.layout.addWidget(self.canvas)
        self.layout.addLayout(self.v_layout)

        #vertical layout for control
        self.v_layout.addWidget(self.button)
        self.v_layout.addWidget(self.general_statment)

        #groupbox for lineEdits
        self.general_statment.setLayout(self.generalStatments_layout)
        self.generalStatments_layout.addWidget(self.set_radius)
        self.generalStatments_layout.addWidget(self.set_diffuse)

        #set the main loyout
        self.setLayout(self.layout)


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
            
        y,x = np.meshgrid(t,r)
        ax.plot_surface(x,y,u)

        ax.set_ylabel("Time, sec")
        ax.set_xlabel("Radius, m")
        ax.set_zlabel("Concentration, mol/liter")

        self.canvas.draw()
        return x,y,u,t,r
    def showMessage(self,event_inniciator):
        if event_inniciator == 'radius_changed':
            try:
                float(self.set_radius.text())
            except ValueError:
                self.messageBox.setText("Incorrect Radius value \nSupported values:  ")
                self.messageBox.show()
            except TypeError:
                self.messageBox.setText("None radius value")
                self.messageBox.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main = Window()
    main.show()

    sys.exit(app.exec_())