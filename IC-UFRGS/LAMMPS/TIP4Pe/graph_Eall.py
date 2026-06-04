import numpy as np
import matplotlib.pyplot as plt


'''
    Plot energy (total, kinetic and potential), temperature, pressure versus timestep.
    Save the mean temperature and pressure in other file (used to plot the phase diagram)
'''

# Energy
def extractData(file, linit, lfinal):

    T = []
    P = []
    K = []
    U = []
    E_tot = []
    t = []

    f = open(file, encoding='utf8')
    
    lines = f.readlines()[linit:lfinal] # ALTERAR CONFORME O ARQUIVO // 1420
    line = []
    i = 0

    while(i < len(lines)):

        line = lines[i].split(' ')
        while('' in line): line.remove('')

        if(line[0] != 'SHAKE'):
            t.append(float(line[0]))
            T.append(float(line[1]))
            #U.append(float(line[2]))
            #K.append(float(line[3]))
            E_tot.append(float(line[3]))
            P.append(float(line[2]))
            i = i + 1

        elif(line[0] == 'SHAKE'):
            i = i + 3
    lim = 100
    
    return t, T, P, E_tot
    
def ALL_graph(t, T, P, E_tot):
    fig = plt.figure(figsize=(12,5))
	
    plt.subplot(131)
    plt.plot(t, E_tot, label='Total')
    plt.xlabel('Time')
    plt.ylabel('Energia (kcal/mol)')
    plt.title('Energias do Sistema')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    plt.subplot(132)    
    plt.plot(t, T)
    plt.xlabel('Time')
    plt.ylabel('T (Kelvin)')
    plt.title('Temperatura do Sistema')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))


    plt.subplot(133)
    plt.plot(t, P)
    plt.xlabel('Time')
    plt.ylabel('P (atm)')
    plt.title('Pressão do Sistema')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    plt.suptitle('rho = 1.05 (g/cm^3)')
    plt.tight_layout()
    plt.show()
    
Tlist = [800, 700, 600, 550, 500]

init = 137
end = 10137

for temp in Tlist:
    file = f'./implicit1/0logT{temp}.lammps'
    
    #if (temp < 1000):
    #    end = 10137
    
    t, T, P, E_tot = extractData(file, init, end)
    ALL_graph(t, T, P, E_tot)