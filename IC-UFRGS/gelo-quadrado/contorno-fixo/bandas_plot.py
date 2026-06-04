import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

N = 9
t = 0.1

pasta = f"./{N}-hopping-{t}"

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
plt.ylabel('Autovalores')
plt.xlabel('Estados')
plt.title(f'Autoenergias - t = {t}')
plt.show()