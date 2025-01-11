import numpy as np
import matplotlib.pyplot as plt

N_radius = 10
N_time = 10
time = 50 #sec
radius = 0.015 #meters
D = 10**-7 #m^2/sec

conc_left = 0
conc_right = 1


dt = time/N_time
t = np.linspace(0,time,N_time+1)

dr = radius/N_radius
r = np.linspace(0,radius,N_radius+1)

a = np.array([0])
b = np.array([0])
c = -D*dt/dr**2
alp = np.array([0])

for i in range (len(r)-1):
    a_1 = (-2*dt*D/(r[i+1]*dr))-(dt*D/dr**2)
    a = np.append(a,a_1)
    b_1 = (1+2*dt*D/(r[i+1]*dr))+2*(dt*D/dr**2)
    b = np.append(b,b_1)
    alp = np.append(alp, -a_1/(b_1 + c*alp[i-1]))



for n in range (0,len(t)):
    if n == 0:
        u = np.array([np.linspace(0, 0, len(r))])
        betta = np.array([np.linspace(0, 0, len(r))])
        continue

    buffer = np.empty(len(r))
    for i in range (0,len(r)):
        buffer = np.append(buffer, (u[n-1][i] + buffer[i-1]*c)/(b[i]+c*alp[i-1]))

    buffer[0] = 0
    betta = np.append(betta,np.array([buffer]))


    buffer = np.empty(len(r))
    for i in range (1,len(r)):
        if i == 1:
            buffer[-i] = conc_right
        else:
            buffer[-i] = buffer[-i+1]*alp[-i]+betta[-i]

    buffer[0] = 0
    u = np.append(u, np.array([buffer]),axis = 0)
y,x = np.meshgrid(r,t)
fig = plt.figure(layout='tight')
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(x, y, u,cmap = 'coolwarm')
plt.show()

