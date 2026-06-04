import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


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

def soma(w, pnm, n, m, Tlist, val, vec):

    wList = []
    chiList = []
    stateList = []
    fParticaoList = []
    
    for T in Tlist:
        
        fParticao = 0
        
        for j in range(len(val)):
        
            fParticao = fParticao + np.exp(-val[j]/T)
        
        fParticaoList.append(fParticao)
    

    for i in range(len(w)):
        
        chi = []
        
        if pnm[i] > 1e-5:
            
            print(i)
            
            for t in range(len(Tlist)):
                    
                chi.append((-1)*pnm[i]*pnm[i]*(np.exp(-val[int(m[i])]/Tlist[t]) - np.exp(-val[int(n[i])]/Tlist[t]))/fParticaoList[t])
                
                
            if w[i] not in wList:
                    
                wList.append(w[i])
                    
                chiList.append(chi)
                    
                stateList.append([n[i], m[i]])
                
            else:
                    
                j = wList.index(w[i])
                    
                stateList[j].append(n[i])
                stateList[j].append(m[i])
                    
                for t in range(len(Tlist)):
                    chiList[j][t] = chiList[j][t] + chi[t]
            
    
    return wList, chiList, stateList



### MAIN ###

N = 9
hop = 0.1
Tlist = [5]
#T = [0.015, 0.05, 0.1, 0.5, 0.8, 1]

pasta = f"./{N}-hopping-{hop}"

val, vec = read_autocoisas(f'{pasta}/{N}_autocoisas.txt')
n, m, Pmn, w = np.loadtxt(f"{pasta}/{N}_Pxxnm.txt", unpack=True)


wList, chiSum, stateList = soma(w, Pmn, n, m, Tlist, val, vec)
plt.scatter(wList, chiSum, s=2)


plt.ylabel(r"$\chi$''")
plt.xlabel(r'Frequência ($w_{nm}$)')

plt.title(f'{N} oxigênios - t = {hop}')
plt.tight_layout()
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), facecolor='white', fontsize=10)
plt.tight_layout()
plt.show()