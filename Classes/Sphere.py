import numpy as np
from PySide6.QtCore import QThread, Signal

class Sphere(QThread):
    def __init__(self, R, D, BaseConc, totalTime, Nradius, N_time, Window):
        QThread.__init__(self)
        self.Window = Window
        self.D = D
        self.R = R
        self.BaseConc = BaseConc
        self.total_time = totalTime
        self.N_time = N_time
        self.N = Nradius
        self.progress = Signal(float)
        self.finished = Signal()

    def SphereDiffusion(self):
        self.r = np.linspace(0, self.R, self.N + 1)  # here N + 1 because otherwise the step will be wrong
        dr = self.R / self.N

        dt = self.total_time / self.N_time
        self.t = np.linspace(0, self.total_time,
                             self.N_time + 1)  # here N + 1 because otherwise the step will be wrong. "0" step is for initial conditions

        self.u = np.zeros((self.N + 1, self.N_time + 1))
        self.u[0:-1, 0] = self.BaseConc

        # main loop
        for tn in range(1, self.N_time + 1):
            # print(tn)
            for j in range(1, self.N):
                self.u[j, tn] = self.D * dt / dr ** 2 * (
                            self.u[j + 1, tn - 1] - 2 * self.u[j, tn - 1] + self.u[j - 1, tn - 1]) + 2 \
                                * self.D * dt / (self.r[j] * dr) * (self.u[j, tn - 1] - self.u[j - 1, tn - 1]) + self.u[
                                    j, tn - 1]

            # boundary conditions
            self.u[0, tn] = self.u[1, tn]
            self.u[-1, tn] = 0

    def MassChanges(self):
        self.mass_on_time = np.zeros_like(self.t)
        for n in range(0, self.N_time + 1):
            mass_on_radius = 0
            for j in range(1, self.N):
                mass_on_radius += (self.r[j] ** 3 - self.r[j - 1] ** 3) * np.pi * self.u[j, n] * 18
            self.mass_on_time[n] = mass_on_radius

    def run(self):
        print('Run')
        self.SphereDiffusion()
        self.MassChanges()

        print("посчитал")
        y, x = np.meshgrid(self.t, self.r)
        z = self.u
        self.Window.surfacePlot.plot(x, y, z)
        print('плоскость есть')
        print(len(self.t), len(self.mass_on_time))
        self.Window.linePlot.plot(self.t, self.mass_on_time)
        print('2д график есть')
