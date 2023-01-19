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
        self.englishLocale = QLocale(QLocale.English)
        # a figure instance to plot on
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        #LineEdit to set solution concetration
        self.set_concetration = QLineEdit()
        self.set_concetration.setPlaceholderText('Input solution concentration')
        self.concetrationValidator = QDoubleValidator()
        self.concetrationValidator.setLocale(self.englishLocale)
        self.set_concetration.setValidator(self.concetrationValidator)

        #LineEdit to set radius by user
        self.set_radius = QLineEdit()
        self.set_radius.setPlaceholderText('Input Radius (meters)')
        self.radiusValidator = QDoubleValidator()
        self.radiusValidator.setLocale(self.englishLocale)
        self.set_radius.setValidator(self.radiusValidator)

        #LineEdit to set diffusion coefficient
        self.set_diffuse = QLineEdit()
        self.set_diffuse.setPlaceholderText('Input Diffusion Coefficient')
        self.coefdiffValidator = QDoubleValidator()
        self.coefdiffValidator.Notation = QDoubleValidator.ScientificNotation
        self.coefdiffValidator.setLocale(self.englishLocale)
        self.set_diffuse.setValidator(self.coefdiffValidator)

        #LineEdit to set time
        self.set_time = QLineEdit()
        self.set_time.setPlaceholderText('Input time (seconds)')
        self.timeeditValidator = QDoubleValidator()
        self.set_time.setLocale(self.englishLocale)
        self.set_time.setValidator(self.timeeditValidator)

        #LineEdit to set nuber of steps by radius
        self.set_radiusSteps = QLineEdit()
        self.set_radiusSteps.setPlaceholderText('Input number of steps by radius')
        self.stepRadiusValidator = QDoubleValidator()
        self.set_radiusSteps.setLocale(self.englishLocale)
        self.set_radiusSteps.setValidator(self.stepRadiusValidator)

        #LineEdit to set nuber of steps by time
        self.set_timeSteps = QLineEdit()
        self.set_timeSteps.setPlaceholderText('Input number of steps by time')
        self.stepTimeValidator = QDoubleValidator()
        self.set_timeSteps.setLocale(self.englishLocale)
        self.set_timeSteps.setValidator(self.stepTimeValidator)

        #button for plot
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)

        #set the layouts
        self.layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.general_statment = QGroupBox(title='General Statments')
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
        self.generalStatments_layout.addWidget(self.set_time)
        self.generalStatments_layout.addWidget(self.set_radiusSteps)
        self.generalStatments_layout.addWidget(self.set_timeSteps)
        self.generalStatments_layout.addWidget(self.set_concetration)

        #set the main loyout
        self.setLayout(self.layout)


    def plot(self):
        self.figure.clear()

        # create an axis
        ax = self.figure.add_subplot(111,projection = '3d')

        #set radius from LineEdit
        try:
            float(self.set_radius.text())
        except BaseException:
            R = 0.015
        else:
            R = float(self.set_radius.text())

        #set Diffusion coeffisient from LineEdit
        try:
            float(self.set_diffuse.text())
        except BaseException:
            D = 10**-6
        else:
            D = float(self.set_diffuse.text())

        # set Number of radius steps from LineEdit
        try:
            float(self.set_radiusSteps.text())
        except BaseException:
            N = 200
        else:
            N = float(self.set_radiusSteps.text())

        # set time from LineEdit
        try:
            float(self.set_time.text())
        except BaseException:
            total_time = 40
        else:
            total_time = float(self.set_radiusSteps.text())
        
        r = np.linspace(0, R, N + 1) # here N + 1 because otherwise the step will be wrong
        dr = R/N


        dt = 0.001 # если тут сделаешь из условия устойчивости расчет - будет круто
        N_time = int(total_time // dt) # integer division, int() is necessary
        t = np.linspace(0, dt * N_time, N_time + 1) # here N + 1 because otherwise the step will be wrong. "0" step is for initial conditions

        u = np.zeros((N + 1, N_time + 1))

        try:
            float(self.set_concetration.text())
        except BaseException:
            u[0:-1, 0] = 1
        else:
            u[0:-1, 0] = float(self.set_concetration.text())

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
    def showMessage(self,event_inniciator):
        #Переработать после добавления всех LineEdit
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