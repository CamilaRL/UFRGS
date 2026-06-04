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

def soma(w, pnm, pmn, n, m, Tlist, val, vec):

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
        
        if w[i] > 0:
            
            chi = []
            
            for t in range(len(Tlist)):
                
                chi.append((-1)*pnm[i]*pmn[i]*(np.exp(-val[int(n[i])]/Tlist[t]) - np.exp(-val[int(m[i])]/Tlist[t]))/fParticaoList[t])
            
            
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
            
    
    return wList, chiList, stateList, fParticaoList


def writeFile(w, T, chi, stateList, pasta):

    f = open(f"{pasta}/chiTempOutput_xy/chiTemp-{w}.txt", "a")
    f.write('# T / chi\n')
    
    f_state_W = open(f'{pasta}/w_state_xy/states-{w}.txt', 'a')
    f_state_W.write('# n / m\n')
    
    for j in range(len(T)):
        f.write(f'{T[j]} {chi[j]}\n')
    
    for i in range(0, len(stateList)-1, 2):
        f_state_W.write(f'{stateList[i]} {stateList[i+1]}\n')
    
    f.close()
    f_state_W.close()



### MAIN ###

N = 4
hop = '1.0'
pasta = f"../Dados_Hop/hopping-{hop}"

Tlist = np.concatenate(( np.arange(0.1, 1, 0.05) , np.arange(1, 5, 0.5) ))

n, m, Pmn, Pnm, w = np.loadtxt(f"{pasta}/{N}_Pxynm.txt", unpack=True)

val, vec = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

wList, chiList, stateList, fParticaoList = soma(w, Pnm, Pmn, n, m, Tlist, val, vec)


fp = open(f"./{pasta}/Z_xy.txt", "w")

for z in range(len(fParticaoList)):
    fp.write(f'{Tlist[z]} {fParticaoList[z]}\n')

fp.close()

for i in range(len(chiList)):
        
        if max(chiList[i]) > 10e-11:
            writeFile(wList[i], Tlist, chiList[i], stateList[i], pasta)
