

import numpy as np 
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
import matplotlib as mpl
R = 10
D = 10**-2


r = np.linspace(0,R,100)
dr = 1/len(r)

dt = dr**2/(2*D*R)
nt = dt**-1
i = 1
t = np.linspace(0,1,int(nt))
while i < nt-1:
    t[i] = t[i-1] + dt
    i+=1


u = np.zeros((len(r),len(t)))


u[0:-1,0] = (10**-2)
u[-1,0] = (10**-2)




for tn in range(1,len(t)-1):
    for hj in range(1,len(r)-1):

      u[hj,tn] = ((D * r[hj] * dt)/(dr * (r[hj]*dr + D * 2 * dt))) * ((u[hj+1,tn-1]-2*u[hj,tn-1] + u[hj-1,tn-1])) + u[hj,tn-1]



ax = plt.figure().add_subplot(projection="3d")
y,x = np.meshgrid(t,r)
ax.plot_surface(x , y , u)


