import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os

## Noxigenios 6
N = 4
hopList = [0.001, 0.005, 0.01, 0.011, 0.012, 0.013, 0.014, 0.015, 0.0155, 0.016, 0.017, 0.018, 0.019, 0.02]
Pol = 'XX'


def Separacao_Cores(hopList, minimo, wAnomalia):

    ## separação por cores
    colors = ['blue', 'purple', 'orange', 'red']
    labels = [r'$\omega$ ~ 0', r'$\omega$ ~ 1', r'$\omega$ ~ 2', r'$\omega$ ~ 3']

    hopList_cores = [[] for i in range(len(colors))]
    minimo_cores = [[] for i in range(len(colors))]

    for k in range(len(wAnomalia)):

        if wAnomalia[k] > 0 and wAnomalia[k] < 0.5:
            hopList_cores[0].append(hopList[k])
            minimo_cores[0].append(minimo[k])
            
        if wAnomalia[k] > 0.5 and wAnomalia[k] < 1.5:
            hopList_cores[1].append(hopList[k])
            minimo_cores[1].append(minimo[k])
            
        if wAnomalia[k] > 1.5 and wAnomalia[k] < 2.5:
            hopList_cores[2].append(hopList[k])
            minimo_cores[2].append(minimo[k])
            
        if wAnomalia[k] > 2.5 and wAnomalia[k] < 3.5:
            hopList_cores[3].append(hopList[k])
            minimo_cores[3].append(minimo[k])
            
    return hopList_cores, minimo_cores, colors, labels



hopPlot = []
TminPlot = []
chiMinPlot = []
wAnomalia = []

# MAIN #
for hop in hopList:
    pasta_chi = f"../{N}oxigenios/hopping-{hop}/chiTempOutput"

    file_anomalia = f"../{N}oxigenios/hopping-{hop}/anomalia.txt"

    wList = np.loadtxt(file_anomalia, unpack=True, usecols=0, ndmin=1)
    Tmin = np.loadtxt(file_anomalia, unpack=True, usecols=1, ndmin=1)
    
    wAnomalia.extend(wList)
    
    for i in range(len(wList)):

        w = wList[i]
        
       
        print(f'{hop} {w}')
        filename = f'{pasta_chi}/chiTemp-{w}.txt'
            
        T, chiT = np.loadtxt(filename, unpack=True)
            
        chiMin = chiT[np.where(T==Tmin[i])]
            
        hopPlot.append(hop)
        TminPlot.append(Tmin[i])
        chiMinPlot.append(chiMin)


hopPlot_cores, TminPlot_cores, cores, labels = Separacao_Cores(hopPlot, TminPlot, wAnomalia)
hopPlot_cores, chiMinPlot_cores, cores, labels = Separacao_Cores(hopPlot, chiMinPlot, wAnomalia)

for k in range(len(cores)):
    plt.scatter(hopPlot_cores[k], chiMinPlot_cores[k], color=cores[k], label=labels[k])
    plt.plot(hopPlot_cores[k], chiMinPlot_cores[k], color=cores[k])

plt.xlabel('Hopping Parameter')
plt.ylabel(r"$\chi$''")
plt.title(f'Minimum Susceptibility')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10)
plt.tight_layout()
plt.show()


for k in range(len(cores)):
    plt.scatter(hopPlot_cores[k], TminPlot_cores[k], color=cores[k], label=labels[k])
    plt.plot(hopPlot_cores[k], TminPlot_cores[k], color=cores[k])

plt.xlabel('Hopping Parameter')
plt.ylabel("Temperature")
plt.title(f'Minimum Temperatures')
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10)
plt.tight_layout()
plt.show()
