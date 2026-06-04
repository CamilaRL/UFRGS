import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

N = 6
t = 0.1

pasta = f"./hopping-{t}"

def read_autocoisas(filename):

    autovetor = []
    autovalor = []
    vetor = []
    i = 0

    with open(filename, "r") as f:
    
        lines = f.readlines()
        autocoisa = lines[0].strip("\n")
        
        for line in lines[1:]:
        
            line = line.strip("\n")
            
            if line == "Autovetores":
                autocoisa = line
            
            elif (autocoisa == "Autovetores") and (line != "Autovetores"):
                
                if(i==len(autovalor)):
                    autovetor.append(vetor)
                    i = 0
                    vetor = []
                    
                vetor.append(float(line))
                i = i + 1
            
            else:
                autovalor.append(float(line))
            
        autovetor.append(vetor)
        
    return autovalor, autovetor


### Main ###

val, vet = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

lista_estados = np.arange(0,len(val))

plt.scatter(lista_estados, val, s=3)
plt.ylabel('Eigenvalues')
plt.xlabel('Eigenstates')
plt.title(f'Eigenvalues of the Hamiltonian - t = {t}')
plt.show()

lista_estados = np.arange(0, len(vet[0]), 1)

print(vet[0][0], vet[0][-1])
print(vet[3][0], vet[3][-1])
print(vet[4][0], vet[4][-1])

plt.scatter(lista_estados, vet[0], s=10, label='0')
plt.scatter(lista_estados, vet[3], s=10, label='3')
plt.scatter(lista_estados, vet[4], s=10, label='4')
plt.xlabel('Estado')
plt.ylabel('Entrada Autovetor')
plt.legend()
plt.show()