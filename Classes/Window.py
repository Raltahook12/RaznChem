from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, \
    QLineEdit, QGroupBox, QFormLayout
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import QLocale, Signal,QSize
from Classes.MplCanvas import MplCanvas
from Classes.Sphere import Sphere


class Window(QWidget):
    finished = Signal()
    progress = Signal(float)

    def __init__(self,screensize, parent=None,):
        super(Window, self).__init__(parent)

        self.setMinimumSize(screensize.width()/2, screensize.height()/2)
        self.englishLocale = QLocale(QLocale.English)

        # a figure instance to plot on
        self.surfacePlot = MplCanvas('3d')
        self.linePlot = MplCanvas()
        self.surfacePlot.setMinimumSize(QSize(screensize.width()/3,screensize.height()/3))
        self.linePlot.setMinimumSize(QSize(screensize.width()/3,screensize.height()/3))

        # button for plot
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.btnPressed)

        # LineEdit to set solution concetration
        self.set_concetration = QLineEdit()
        self.set_concetration.setPlaceholderText('Input solution concentration')
        self.concetrationValidator = QDoubleValidator()
        self.concetrationValidator.setLocale(self.englishLocale)
        self.set_concetration.setValidator(self.concetrationValidator)

        # LineEdit to set radius by user
        self.set_radius = QLineEdit()
        self.set_radius.setPlaceholderText('Input Radius (meters)')
        self.radiusValidator = QDoubleValidator()
        self.radiusValidator.setLocale(self.englishLocale)
        self.set_radius.setValidator(self.radiusValidator)

        # LineEdit to set diffusion coefficient
        self.set_diffuse = QLineEdit()
        self.set_diffuse.setPlaceholderText('Input Diffusion Coefficient')
        self.coefdiffValidator = QDoubleValidator()
        self.coefdiffValidator.Notation = QDoubleValidator.ScientificNotation
        self.coefdiffValidator.setLocale(self.englishLocale)
        self.set_diffuse.setValidator(self.coefdiffValidator)

        # LineEdit to set time
        self.set_time = QLineEdit()
        self.set_time.setPlaceholderText('Input time (seconds)')
        self.timeeditValidator = QDoubleValidator()
        self.set_time.setLocale(self.englishLocale)
        self.set_time.setValidator(self.timeeditValidator)

        # LineEdit to set nuber of steps by radius
        self.set_radiusSteps = QLineEdit()
        self.set_radiusSteps.setPlaceholderText('Input number of steps by radius')
        self.stepRadiusValidator = QDoubleValidator()
        self.set_radiusSteps.setLocale(self.englishLocale)
        self.set_radiusSteps.setValidator(self.stepRadiusValidator)

        # LineEdit to set nuber of steps by time
        self.set_timeSteps = QLineEdit()
        self.set_timeSteps.setPlaceholderText('Input number of steps by time')
        self.stepTimeValidator = QDoubleValidator()
        self.set_timeSteps.setLocale(self.englishLocale)
        self.set_timeSteps.setValidator(self.stepTimeValidator)

        # set the layouts
        self.layout = QHBoxLayout()
        self.v_layout = QVBoxLayout()
        self.graphLayout = QVBoxLayout()
        self.general_statment = QGroupBox(title='General Statments')
        self.generalStatments_layout = QFormLayout()
        self.selectionbox = QGroupBox(title='Selection properties')

        # add Widgets to layouts
        # main layout
        self.layout.addLayout(self.graphLayout)
        self.layout.addLayout(self.v_layout)

        # vertical layout for plots
        self.graphLayout.addWidget(self.surfacePlot)
        self.graphLayout.addWidget(self.linePlot)

        # vertical layout for control
        self.v_layout.addWidget(self.button)
        self.v_layout.addWidget(self.general_statment)
        self.v_layout.addWidget(self.selectionbox)

        # groupbox for lineEdits
        self.general_statment.setLayout(self.generalStatments_layout)
        self.generalStatments_layout.addWidget(self.set_radius)
        self.generalStatments_layout.addWidget(self.set_diffuse)
        self.generalStatments_layout.addWidget(self.set_time)
        self.generalStatments_layout.addWidget(self.set_radiusSteps)
        self.generalStatments_layout.addWidget(self.set_timeSteps)
        self.generalStatments_layout.addWidget(self.set_concetration)

        # set the main loyout
        self.setLayout(self.layout)
        print()

    def readDatas(self):
        # set radius from LineEdit

        try:
            float(self.set_radisus.text())
        except BaseException:
            R = 0.015
        else:
            R = float(self.set_radius.text())

        # set Diffusion coeffisient from LineEdit
        try:
            float(self.set_diffuse.text())
        except BaseException:
            D = 10 ** -6
        else:
            D = float(self.set_diffuse.text())

        # set Number of radius steps from LineEdit
        try:
            float(self.set_radiusSteps.text())
        except BaseException:
            Nradius = 200
        else:
            Nradius = float(self.set_radiusSteps.text())

        # set time from LineEdit
        try:
            float(self.set_time.text())
        except BaseException:
            totalTime = 40
        else:
            totalTime = float(self.set_time.text())
        # set base concentration in sphere from lineedit
        try:
            float(self.set_concetration.text())
        except BaseException:
            BaseConc = 1
        else:
            BaseConc = float(self.set_concetration.text())
        # set Number of steps by time from LineEdit
        try:
            float(self.set_timeSteps.text())
        except BaseException:
            N_time = 40000
        else:
            N_time = float(self.set_timeSteps.text())

        return R, D, BaseConc, totalTime, Nradius, N_time

    def btnPressed(self):
        R, D, BaseConc, totalTime, Nradius, N_time = self.readDatas()
        self.sphere = Sphere(R, D, BaseConc, totalTime, Nradius, N_time, self)
        print('plot')
        self.sphere.start()

    def showMessage(self, event_inniciator):
        # Переработать после добавления всех LineEdit
        if event_inniciator == 'radius_changed':
            try:
                float(self.set_radius.text())
            except ValueError:
                self.messageBox.setText("Incorrect Radius value \nSupported values:  ")
                self.messageBox.show()
            except TypeError:
                self.messageBox.setText("None radius value")
                self.messageBox.show()