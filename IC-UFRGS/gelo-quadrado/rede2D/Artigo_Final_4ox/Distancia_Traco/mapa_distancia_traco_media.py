import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

N = 4
size = 256
hopList = [0.0001, 0.001, 0.01, 0.05, 0.1]
traco_medioList = []

for t in hopList:

    pasta = f"../Dados_Hop/hopping-{t}"

    trace_matrix = np.loadtxt(f"{pasta}/mapa_traco_{t}.txt", unpack=True, usecols=range(size))

    traco_medio = 0
    elementos = 0
    
    for i in range(len(trace_matrix)):
        for j in range(len(trace_matrix[i])):
        
            traco_medio = traco_medio + trace_matrix[i][j]
            elementos = elementos + 1
            
    traco_medio = traco_medio/elementos
    
    traco_medioList.append(traco_medio)
    
plt.scatter(hopList, traco_medioList, s=10)
plt.plot(hopList, traco_medioList)
plt.xscale('log')
plt.ylabel("Mean Trace Distance")
plt.xlabel("Hopping Parameter")
plt.show()