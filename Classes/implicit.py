import numpy as np
import matplotlib.pyplot as plt

N_radius = 10
N_time = 10
time = 60*30 #sec
radius = 0.015 #meters
D = 10**-9 #m^2/sec

conc_left = 1
conc_right = 1



def NRS(N_radius , N_time , time , radius , D , conc_left, conc_right,CR = 'left'):
    """Неявная разностная схема, возможно использовать различные варианты схемы расчёта заданием параметра CR ('left','right',
        'middle' для левой,правой и центральной конечной разности соответственно), default: CR = 'left'"""

    t = np.linspace(0,time,N_time+1)

    r = np.linspace(0,radius,N_radius+1)

    dr = radius/N_radius
    dt = time/N_time

    a = np.array([0])
    b = np.array([0])
    c = np.array([0])
    alp = np.array([0])

    match CR:
        case "left":
            for i in range (1,len(r)):
                a = np.append(a,-D * dt / dr**2)
                b = np.append(b,1 + 2 * dt * D / dr**2 - 2 * dt * D / ( r[i] * dr ))
                c = np.append(c,-D * dt / dr**2 + 2 * D * dt /( r[i] * dr ))
                alp = np.append(alp, -a[i]/(b[i] + c[i]*alp[i-1]))

        case "right":
            for i in range (1,len(r)):
                a = np.append(a,(-2*dt*D/(r[i]*dr))-(dt*D/dr**2))
                b = np.append(b,(1+2*dt*D/(r[i]*dr))+2*dt*D/dr**2)
                c = np.append(c,-D * dt / dr ** 2)
                alp = np.append(alp, -a[i]/(b[i] + c[i]*alp[i-1]))

        case "middle":
            for i in range (1,len(r)):
                a = np.append(a,((-dt*D)/(r[i]*dr))-((dt*D)/(dr**2)))
                b = np.append(b,(1+(2*dt*D)/(dr**2)))
                c = np.append(c, (-(dt*D/(dr**2)+(dt*D)/(r[i]*dr))))
                alp = np.append(alp, -a[i]/(b[i] + c*alp[i-1]))

    def runConvergence(a,b,c): #проверка сходимости
         for i in range(1,len(r)):
            if abs(a[i]) + abs(c[i]) < abs(b[i]):
                pass
            else:
                return('Break')

    if runConvergence(a,b,c) == 'Break':
        return print('Прогонка не сходится')

    for n in range(0, len(t)):
        if n == 0:
            # начальные условия
            u = np.array([np.linspace(conc_left, conc_left, len(r))])
            betta = np.array([np.linspace(conc_left, conc_left, len(r))])
            continue

        buffer = np.empty(len(r))
        for i in range(0, len(r)):
            match i:
                case 0:
                    buffer[i] = conc_left  # граничное условие
                case _:
                    buffer[i] = (u[n - 1][i] + buffer[i - 1] * c[i]) / (b[i] + c[i] * alp[i - 1])
        betta = np.append(betta, np.array([buffer]), axis=0)

        buffer = np.empty(len(r))
        for i in range(1, len(r)):
            if i == 1:
                buffer[-i] = conc_right #граничное условие
            else:
                buffer[-i] = buffer[-i + 1] * alp[-i] + betta[n][-i]
        buffer[0] = conc_left #граничное условие
        u = np.append(u, np.array([buffer]), axis=0)
    print(a,b,c)
    print(alp)
    print(betta)
    print(u)
    y,x = np.meshgrid(r,t)
    fig = plt.figure(layout='tight')
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, u,cmap = 'coolwarm')
    plt.show()


NRS(N_radius , N_time , time , radius , D , conc_left, conc_right)
NRS(N_radius , N_time , time , radius , D , conc_left, conc_right,CR = "right")
NRS(N_radius , N_time , time , radius , D , conc_left, conc_right,CR = "middle")

