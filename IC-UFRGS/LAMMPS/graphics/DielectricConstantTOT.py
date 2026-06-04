import numpy as np
import matplotlib.pyplot as plt

def plot_DielectricTemperature(file):
    
    T, e = np.loadtxt(file, unpack=True)
    
    eref = [90, 79, 73]
    
    plt.scatter(T, e, label=r'$\rho$ = 1.05 g/cm^3')
    plt.plot(T, e, linewidth=0.5)
    plt.scatter([280, 300, 320], eref, color='black', label=r'$\rho_{ref}$ = 1.00 g/cm^3')
    plt.plot([280, 300, 320], eref, color='black', linewidth=0.5)
    plt.ylabel(r'$\epsilon$')
    plt.xlabel('T (K)')
    plt.title('Contante Dielétrica')
    #plt.ylim(bottom=30, top=130)
    #plt.xlim(left=220, right=330)
    plt.legend()
    plt.show()
    
def read_DipoleData(filename):

    mux = []
    muy = []
    muz = []

    with open(filename, 'r') as f:

        lines = f.readlines()[4:]

        for i in range(len(lines)-3):

            mux.append(float(lines[i].split(' ')[1])*angs*1.6*(10**-19)) # C.m
            muy.append(float(lines[i+1].split(' ')[1])*angs*1.6*(10**-19))
            muz.append(float(lines[i+2].split(' ')[1])*angs*1.6*(10**-19))

            i = i + 4

        return mux, muy, muz


def plot_Dipole(mux, muy, muz, T):

    mu = []
    time = []
    for i in range(len(mux)):
        mu.append((mux[i]**2 + muy[i]**2 + muz[i]**2)**(1/2))
        time.append(i)

    plt.plot(time, mu)
    plt.xlabel('Time (fs)')
    plt.ylabel('M (C.m)')
    plt.title(f'Momento de dipolo total (T = {T}K)')
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
    #Mvar = (M2/time)
    
    print(M2/time)
    print((Mmean/time)**2)

    e = 1 + (4*np.pi*Mvar)/(3*e0*kB*V*T) #4*np.pi*
    
    print(f'{T} {e}')
    
def graph_M():

    mu = np.loadtxt("./npt/dipole.txt", unpack=True)

    time = np.arange(len(mu))

    plt.plot(time, mu)
    plt.xlabel("Time")
    plt.ylabel("M")
    plt.title("Momento de Dipolo")
    plt.show()
    
    return mu

def save_M(mu):

    with open("./npt/dipole.txt", "a") as f:
        
        for m in mu:
            f.write(f"{m}\n")
        
    f.close()


global angs

avogadro = 6.022*(10**23)
angs = 10**(-10)




number_files = int(input('Número de arquivos analisados: '))

for i in range(number_files):

    file = input('Arquivo dipoleMoment.sh: ')
    T = int(input('Temperatura: '))
    Nmol = int(input('Número de moléculas: '))
    #V = float(input('Volume Médio: ')) # Angstrom = 10^-24 cm^3
    
    #V = V*10**(-30) # m^3
    
    rho = float(input('Densidade Média: ')) #0.94213664 #g/cm^3
    lbox = (10**-2)*(Nmol * (2 * 1.008 + 15.99)/(rho * avogadro))**(1/3) # m
    V = (lbox)**3
    
    if(i == 0):
        mux, muy, muz = read_DipoleData(file)

    if(i > 0):
        mxaux, myaux, mzaux = read_DipoleData(file)
        
        mux = mux + mxaux
        muy = muy + myaux
        muz = muz + mzaux


mu = plot_Dipole(mux[:], muy[:], muz[:], T)

dielectric_constante(mu, V, T)