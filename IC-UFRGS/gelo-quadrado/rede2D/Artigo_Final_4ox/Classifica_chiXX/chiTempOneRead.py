import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import os

## Noxigenios 6
N = 4
hop = 0.1

# MAIN #

pasta_chi = f"../Dados_Hop/hopping-{hop}/chiTempOutput"

w = 1.207693312868122
    
filename = f'{pasta_chi}/chiTemp-{w}.txt'
        
T, chiT = np.loadtxt(filename, unpack=True)

       
plt.scatter(T, chiT, s=2)
plt.plot(T, chiT, label=f't = {hop} (W ~ {w:.6f})')


plt.xlabel('Temperature')
plt.ylabel(r"$\chi$''")
#plt.grid(True)
plt.legend() #loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10
#plt.xscale('log')
plt.tight_layout()
plt.show()