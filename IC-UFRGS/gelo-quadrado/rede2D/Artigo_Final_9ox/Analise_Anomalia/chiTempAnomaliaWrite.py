import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os

## Noxigenios 6
N = 4
hop = 0.2

def minimo(chi, temp, w):

    chi = np.array(chi)
    found_min = False

    f = open(f"./{N}oxigenios/hopping-{hop}/anomalia.txt", 'a')
    
    for i in range(1, len(chi)-1, 1):
    
    
        if chi[i] < chi[i-1] and chi[i] < chi[i+1]:
            print(f'{chi[i-1]} {chi[i]} {chi[i+1]}')
            found_min = True
            f.write(f"{w} {temp[i]}\n")
            
    f.close()
    
    return found_min


# MAIN #

pasta = f"./{N}oxigenios/hopping-{hop}/chiTempOutput"

path = f'{pasta}/'

files = []
wList = []

for i in os.listdir(path):

    if os.path.isfile(os.path.join(path,i)) and 'chiTemp-' in i:
    
        files.append(i)
        wList.append(float(i.replace(f'chiTemp-','').replace('.txt', '')))

wList, files = (list(t) for t in zip(*sorted(zip(wList, files))))

color = iter(cm.rainbow(np.linspace(0, 1, len(files))))

for i in range(len(files)):

    filename = f'{path}{files[i]}'
    w = wList[i]
    
    T, chiT = np.loadtxt(filename, unpack=True)
    
    c = next(color)
    
    if w > 0:
        if minimo(chiT, T, w):
            plt.scatter(T, chiT, color=c, s=2)
            plt.plot(T, chiT, color=c, label=f't = {hop} (W ~ {w:.6f})')
            print(w)

plt.xlabel('Temperature')
plt.ylabel(r"$\chi$''")
plt.legend() #loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10
#plt.xscale('log')
plt.tight_layout()
plt.show()