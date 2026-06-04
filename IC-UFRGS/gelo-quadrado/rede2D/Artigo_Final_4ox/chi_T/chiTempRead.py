import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os


# MAIN #

## Noxigenios 6
N = 4
hop = 0.001

pasta_chi = f"../Dados_Hop/hopping-{hop}/chiTempOutput"

path = f'{pasta_chi}/'

files = []
wList = []

for i in os.listdir(path):

    if os.path.isfile(os.path.join(path,i)) and 'chiTemp-' in i:
    
        files.append(i)
        wList.append(float(i.replace(f'chiTemp-','').replace('.txt', '')))

wList, files = (list(t) for t in zip(*sorted(zip(wList, files))))

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
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10) #
plt.tight_layout()
plt.show()