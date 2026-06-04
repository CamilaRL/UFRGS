import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm



def Read_File_Matrix(file, dtype):
    
    
    with open(file, 'r') as f:
        
        lines = f.readlines()
        
        N = len(lines)
        
        if dtype == 'str':
            matrix = [['' for j in range(N)] for i in range(N)]
            
        elif dtype == 'int':
            matrix = np.zeros((N, N))
        
        for l in range(N):
            
            line = lines[l].strip("\n").split(',')
            
            for k in range(len(line)-1):
                
                matrix[l][k] = line[k]
    
    
    return matrix

N = 4
size = 256
hop = 0.1

matriz_formato = Read_File_Matrix(f'../Dados_Hop/hopping-{hop}/operador_ciclo/matriz_formato.txt', 'str')

matriz_teve_tunelamento = Read_File_Matrix(f'../Dados_Hop/hopping-{hop}/operador_ciclo/matriz_teve_tunelamento.txt', 'int')

matriz_ordem = Read_File_Matrix(f'../Dados_Hop/hopping-{hop}/operador_ciclo/matriz_ordem.txt', 'int')

matriz_numero_conectados = Read_File_Matrix(f'../Dados_Hop/hopping-{hop}/operador_ciclo/matriz_numero_conectados.txt', 'int')



### FORMATO ###
for i in range(size):
    for j in range(size):
        
        m = matriz_formato[i][j]
        
        if m == 'aberto':
            matriz_formato[i][j] = 1
        
        elif m == 'fechado desordenado':
            matriz_formato[i][j] = 2
        
        elif m == 'fechado ordenado':
            matriz_formato[i][j] = 3
        
        else:
            matriz_formato[i][j] = 0


fig = plt.figure(figsize=(8,8))
cmap = cm.get_cmap('viridis', 4)
image = plt.imshow(matriz_formato, cmap=cmap, aspect='equal', origin='lower', vmin=0)

plt.yticks(ticks=np.arange(0, size, 10), fontsize=8)
plt.xticks(ticks=np.arange(0, size, 10), rotation=90, fontsize=8)

cbar = fig.colorbar(image, orientation='horizontal')
cbar.set_ticks(ticks=[0, 1, 2, 3], labels=['No Tunnelling', 'Open', 'Disordered Closed', 'Ordered Closed'])

plt.title(f'Tunnelling Classification | {N} oxygens | t = {hop}')
plt.ylabel('Eigenstate')
plt.xlabel('Eigenstate')
plt.tight_layout()
plt.show()



### TEVE TUNELAMENTO ###

cmap = cm.get_cmap('viridis', 2)

image = plt.imshow(matriz_teve_tunelamento, cmap=cmap, aspect='equal', origin='lower', vmin=0)

plt.yticks(ticks=np.arange(0, size, 10), fontsize=8)
plt.xticks(ticks=np.arange(0, size, 10), rotation=90, fontsize=8)
plt.colorbar(ticks=[0,1])
plt.title(f'Tunnelling Occurrence | {N} oxygens | t = {hop}')
plt.ylabel('Eigenstate')
plt.xlabel('Eigenstate')
plt.tight_layout()
plt.show()


### ORDEM ###

image = plt.imshow(matriz_ordem, cmap='viridis', aspect='equal', origin='lower', vmin=0)

plt.yticks(ticks=np.arange(0, size, 10), fontsize=8)
plt.xticks(ticks=np.arange(0, size, 10), rotation=90, fontsize=8)
plt.colorbar()
plt.title(f'Tunnelling Order | {N} oxygens | t = {hop}')
plt.ylabel('Eigenstate')
plt.xlabel('Eigenstate')
plt.tight_layout()
plt.show()


### NUMERO H CONECTADOS ###

image = plt.imshow(matriz_numero_conectados, cmap='viridis', aspect='equal', origin='lower', vmin=0)

plt.yticks(ticks=np.arange(0, size, 10), fontsize=8)
plt.xticks(ticks=np.arange(0, size, 10), rotation=90, fontsize=8)
plt.colorbar()
plt.title(f'Number of Connected Hydrogens | {N} oxygens | t = {hop}')
plt.ylabel('Eigenstate')
plt.xlabel('Eigenstate')
plt.tight_layout()
plt.show()
