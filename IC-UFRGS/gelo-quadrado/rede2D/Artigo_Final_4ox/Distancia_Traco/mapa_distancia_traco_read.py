import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

N = 4
size = 256
t = 0.001
T = 0.1

pasta = f"../Dados_Hop/hopping-{t}"

trace_matrix = np.loadtxt(f"{pasta}/mapa_traco_{t}_{T}.txt", unpack=True, usecols=range(size))

image = plt.imshow(trace_matrix, cmap='viridis', aspect='equal', origin='lower', vmin=0)

plt.yticks(ticks=np.arange(0, size+1, 10), fontsize=8)
plt.xticks(ticks=np.arange(0, size+1, 10), rotation=90, fontsize=8)
plt.colorbar()
plt.title(f'Trace Distance | {N} oxygens | t = {t}')
plt.ylabel('Eigenstate')
plt.xlabel('Eigenstate')
plt.tight_layout()
plt.show()