import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os

## Noxigenios 6
N = 4
hop = 0.001
Pol = 'XX'

# MAIN #

pasta_chi = f"../{N}oxigenios/hopping-{hop}/chiTempOutput"

file_anomalia = f"../{N}oxigenios/hopping-{hop}/anomalia.txt"

wList = np.loadtxt(file_anomalia, unpack=True, usecols=(0), ndmin=1)

color = iter(cm.rainbow(np.linspace(0, 1, len(wList))))

for i in range(len(wList)):

    w = wList[i]
    
    filename = f'{pasta_chi}/chiTemp-{w}.txt'
    
    T, chiT = np.loadtxt(filename, unpack=True)

    c = next(color)
    
    plt.scatter(T, chiT, color=c, s=2)
    plt.plot(T, chiT, color=c, label=f't = {hop} (W ~ {w:.6f})')
    print(w)


plt.xlabel('Temperature')
plt.ylabel(r"$\chi$''")
plt.title(f'Polarization')
#plt.grid(True)
plt.legend() #loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10
#plt.xscale('log')
plt.tight_layout()
plt.show()