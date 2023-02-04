import sys
import numpy as np
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QVBoxLayout,QHBoxLayout,\
                            QLabel,QLineEdit,QGroupBox,QFormLayout,QMessageBox
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import QLocale
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg 
import matplotlib.pyplot as plt


class Window(QWidget):

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        self.setMinimumSize(1200,800)
        self.englishLocale = QLocale(QLocale.English)

        # a figure instance to plot on
        self.surfacePlot = MplCanvas('3d')
        self.linePlot = MplCanvas()
        

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
        self.graphLayout = QVBoxLayout()
        self.general_statment = QGroupBox(title='General Statments')
        self.generalStatments_layout = QFormLayout()
        self.selectionbox = QGroupBox(title = 'Selection properties')

        #add Widgets to layouts
        #main layout
        self.layout.addLayout(self.graphLayout)
        self.layout.addLayout(self.v_layout)

        #vertical layout for plots
        self.graphLayout.addWidget(self.linePlot)
        self.graphLayout.addWidget(self.surfacePlot)

        #vertical layout for control
        self.v_layout.addWidget(self.button)
        self.v_layout.addWidget(self.general_statment)
        self.v_layout.addWidget(self.selectionbox)
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
        print()


    def SphereDiffusion(self):

        #set radius from LineEdit
        try:
            float(self.set_radisus.text())
        except BaseException:
            self.R = 0.015
        else:
            self.R = float(self.set_radius.text())

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
            self.N = 200
        else:
            self.N = float(self.set_radiusSteps.text())

        # set time from LineEdit
        try:
            float(self.set_time.text())
        except BaseException:
            total_time = 40
        else:
            total_time = float(self.set_time.text())
        
        self.r = np.linspace(0, self.R, self.N + 1) # here N + 1 because otherwise the step will be wrong
        dr = self.R/self.N


        dt = 0.001 # если тут сделаешь из условия устойчивости расчет - будет круто
        self.N_time = int(total_time // dt) # integer division, int() is necessary
        self.t = np.linspace(0, dt * self.N_time, self.N_time + 1) # here N + 1 because otherwise the step will be wrong. "0" step is for initial conditions

        self.u = np.zeros((self.N + 1, self.N_time + 1))
        

        try:
            float(self.set_concetration.text())
        except BaseException:
            self.u[0:-1, 0] = 1
        else:
            self.u[0:-1, 0] = float(self.set_concetration.text())
        # main loop
        for tn in range(1, self.N_time + 1):
            # print(tn)
            for j in range(1, self.N):
                self.u[j, tn] = D * dt / dr ** 2 * (self.u[j + 1, tn - 1] - 2 * self.u[j, tn - 1] + self.u[j - 1, tn - 1]) + 2 \
                           * D * dt / (self.r[j] * dr) * (self.u[j, tn - 1] - self.u[j - 1, tn - 1]) + self.u[j, tn - 1]

            # boundary conditions
            self.u[0, tn] = self.u[1, tn]
            self.u[-1,tn] = 0



    def MassChanges(self):
        self.mass_on_time = np.zeros_like(self.t)
        for n in range(0,self.N_time + 1):
            mass_on_radius = 0
            for j in range(1,self.N):
                mass_on_radius += (self.r[j]**3-self.r[j-1]**3)*np.pi*self.u[j,n]*18
            self.mass_on_time[n] = mass_on_radius
    
    def plot(self):
        self.SphereDiffusion()
        self.MassChanges()

        print("посчитал")
        y,x = np.meshgrid(self.t,self.r)
        z = self.u
        self.surfacePlot.plot(x,y,z)
        print('плоскость есть')
        self.linePlot.plot(self.t,self.mass_on_time)
        print('2д график есть')

        
    
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

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self,proj = None):
        if proj is None:
            self.fig = plt.figure(layout='tight')
            self.ax = self.fig.add_subplot(111)
            super(MplCanvas, self).__init__(self.fig)
        elif proj == '3d':
            self.fig = plt.figure(layout='tight')
            self.ax = self.fig.add_subplot(111,projection = '3d')
            super(MplCanvas, self).__init__(self.fig)
    def plot(self,x,y,z = None):
        if z is None:
            with plt.ion():
                self.ax.plot(x,y)

                self.ax.set_xlabel("Mass, g")
                self.ax.set_ylabel("Time, sec")

        else:
            with plt.ion():
                self.ax.plot_surface(x, y, z)

                self.ax.set_ylabel("Time, sec")
                self.ax.set_xlabel("Radius, m")
                self.ax.set_zlabel("Concentration, mol/liter")

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    main = Window()
    main.show()

    sys.exit(app.exec_())