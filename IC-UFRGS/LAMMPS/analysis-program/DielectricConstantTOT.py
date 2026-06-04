import numpy as np
import matplotlib.pyplot as plt

def plot_DielectricTemperature(file):
    
    T, e = np.loadtxt(file, unpack=True)
    
    eref = [90, 79, 73]
    
    plt.scatter(T, e, label=r'$\rho$ = 1.05 g/cm^3')
    plt.plot(T, e, linewidth=0.5)
    plt.scatter(T, eref, color='black', label=r'$\rho$ = 1.00 g/cm^3')
    plt.plot(T, eref, color='black', linewidth=0.5)
    plt.ylabel(r'$\epsilon$')
    plt.xlabel('T (K)')
    plt.title('Contante Dielétrica')
    plt.ylim(bottom=30, top=130)
    plt.xlim(left=220, right=330)
    plt.legend()
    plt.show()
    
def read_DipoleData(filename):

    mux = []
    muy = []
    muz = []

    with open(filename, 'r') as f:

        lines = f.readlines()[4:]

        for i in range(len(lines)-3):

            mux.append(float(lines[i].split(' ')[1])*angs*1.6*(10**-19))
            muy.append(float(lines[i+1].split(' ')[1])*angs*1.6*(10**-19))
            muz.append(float(lines[i+2].split(' ')[1])*angs*1.6*(10**-19))

            i = i + 4

        return mux, muy, muz


def plot_Dipole(mux, muy, muz):

    mu = []
    time = []
    for i in range(len(mux)):
        mu.append((mux[i]**2 + muy[i]**2 + muz[i]**2)**(1/2))
        time.append(i)

    plt.plot(time, mu)
    plt.xlabel('Time (fs)')
    plt.ylabel('M (C.m)')
    plt.title('Momento de dipolo total')
    plt.show()

    return mu

def dielectric_constante(mu, V, T):

    kB = 1.38*(10**(-23))
    e0 = 8.85*(10**(-12))

    M2 = 0
    Mmean = 0
    for m in mu:
        M2 = M2 + m*m
        Mmean = Mmean + m
        
    time = len(mu)

    Mvar = (M2/time) - (Mmean/time)**2
    
    #e = 1 + (Mvar)/(3*e0*kB*V*T)
    #e = 1 + (4*np.pi*Mvar)/(3*kB*V*T)
    e = 1 + (4*np.pi*Mvar)/(3*e0*kB*V*T)
    
    print(f'{T} {e}')

global angs

angs = 10**(-10)
lbox = 14.2*angs
V = lbox**3
T = 280

'''mux, muy, muz = read_DipoleData(f'./implicit/3dipoleMomentT{T}.sh')
mu = plot_Dipole(mux, muy, muz)


dielectric_constante(mu, V, T)'''

plot_DielectricTemperature('./implicit/dielectric.txt')



