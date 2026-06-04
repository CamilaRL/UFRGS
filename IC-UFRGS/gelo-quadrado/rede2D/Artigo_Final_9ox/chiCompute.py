import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

N = 4
hop = 0.1
T = [0.1]
#T = [0.015, 0.05, 0.1, 0.5, 0.8, 1]

pasta = f"./{N}oxigenios/hopping-{hop}"

n, m, Pmn, Pnm, w = np.loadtxt(f"{pasta}/{N}_Pnm.txt", unpack=True)

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

def soma(w, peso, n, m, T):
    val, vec = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

    chiSum = [(-1)*peso[0]*peso[0]*(np.exp(-val[int(n[0])]/T) - np.exp(-val[int(m[0])]/T))]
    wList = [w[0]]
    stateList = [[n[0], m[0]]]
    fParticao = 0
    

    for i in range(1,len(w)):
        
        if w[i] not in wList:

            wList.append(w[i])
            chiSum.append((-1)*peso[i]*peso[i]*(np.exp(-val[int(n[i])]/T) - np.exp(-val[int(m[i])]/T)))
            stateList.append(n[i])
            stateList.append(m[i])
            
        else:
            
            j = wList.index(w[i])
            chiSum[j] = chiSum[j] + (-1)*peso[i]*peso[i]*(np.exp(-val[int(n[i])]/T) - np.exp(-val[int(m[i])]/T))
            stateList.append(n[i])
            stateList.append(m[i])
    
        fParticao = fParticao + np.exp(-val[int(n[i])]/T)
    
    wList, chiSum = (list(t) for t in zip(*sorted(zip(wList, chiSum))))
    
    chiSum = chiSum/fParticao
    
    return wList, chiSum, stateList



for t in T:
    wList, chiSum, stateList = soma(w, Pnm, n, m, t)
    plt.scatter(wList, chiSum, s=2)
    plt.plot(wList, chiSum, linewidth=1, label=f"T={t}")


plt.ylabel(r"$\chi$''")
plt.xlabel(r'Frequência ($w_{nm}$)')

plt.title(f'{N} oxigênios - t = {hop}')
plt.tight_layout()
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10)
plt.tight_layout()
plt.show()