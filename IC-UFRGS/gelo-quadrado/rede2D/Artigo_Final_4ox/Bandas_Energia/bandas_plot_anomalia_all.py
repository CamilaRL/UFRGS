import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


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

N = 4
t = 1.0

pasta = f"../Dados_Hop/hopping-{t}"

wAll = np.loadtxt(f'../Classifica_chiXY/classificacao-hop{t}.txt', unpack=True, usecols=(0))
classeAll = np.loadtxt(f'../Classifica_chiXY/classificacao-hop{t}.txt', unpack=True, usecols=(1), dtype='str')

wList = []
for i, classe in enumerate(classeAll):
    
    if classe == 'anomala':
        wList.append(wAll[i])
    
cores = iter(cm.YlOrRd(np.linspace(0, 1, len(wList))))

val, vet = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

lista_estados = np.arange(0,len(val))

plt.scatter(lista_estados, val, s=3)

for w in wList:
    nList, mList = np.loadtxt(f'{pasta}/w_state_xy/states-{w}.txt', unpack=True)
    cor = next(cores)
    for i, n in enumerate(nList):
    
        nm = [int(n), int(mList[i])]
        
        i_f_val = []
        
        i_f_val.append(val[int(n)])
        i_f_val.append(val[int(mList[i])])

        print(i_f_val[0] - i_f_val[1])
        
        plt.scatter(nm, i_f_val, color=cor)
        plt.plot(nm, i_f_val, color=cor)
        

plt.ylabel('Eigenvalues')
plt.xlabel('Eigenstates')
plt.title(f'Eigenvalues of the Hamiltonian - t = {t}')
plt.show()