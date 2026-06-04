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

def soma(w, wList, pnm, pmn, n, m, Tlist, val, vec):

    fParticaoList = []
    
    for T in Tlist:
        
        fParticao = 0
        
        for j in range(len(val)):
        
            fParticao = fParticao + np.exp(-val[j]/T)
        
        fParticaoList.append(fParticao)
    
    iList = []
    
    for i, wi in enumerate(wList):
        
        if w == wi:
            iList.append(i)
    
    print(iList)
    for i in iList:
        
        chi = []
                
        for t in range(len(Tlist)):
                
            chi.append((-1)*pnm[i]*pmn[i]*(np.exp(-val[int(n[i])]/Tlist[t]) - np.exp(-val[int(m[i])]/Tlist[t]))/fParticaoList[t])
           
        plt.plot(Tlist, chi, label=f'{int(n[i])} -> {int(m[i])}')
    
    plt.xlabel('Temperature')
    plt.ylabel(r"$\chi$''")
    plt.title(f'Frequency: {w}')
    plt.legend()
    plt.show()



### MAIN ###

N = 4
hop = '0.1'
pasta = f"../Dados_Hop/hopping-{hop}"

w = 1.2076933128681158

Tlist = np.concatenate(( np.arange(0.01, 1, 0.05) , np.arange(1, 5, 0.5) ))

n, m, Pmn, Pnm, wList = np.loadtxt(f"{pasta}/{N}_Pxxnm.txt", unpack=True)

val, vec = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

soma(w, wList, Pnm, Pmn, n, m, Tlist, val, vec)
