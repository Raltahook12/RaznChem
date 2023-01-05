import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

R = 0.01 # m
D = 10**-6 # m2/s
N = 100 # R steps Number
total_time = 10 # s

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

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

y, x = np.meshgrid(t, r)
ax.plot_surface(x, y, u, cmap=cm.coolwarm,
linewidth=0, antialiased=False)

ax.set_xlabel('Gel radius')
ax.set_ylabel('Time, s')
ax.view_init(-160, 60)

plt.show()


