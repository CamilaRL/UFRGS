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

def soma(w, pnm, pmn, n, m, T):

    val, vec = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

    chiSum = [(-1)*pnm[0]*pmn[0]*(np.exp(-val[int(n[0])]/T) - np.exp(-val[int(m[0])]/T))]
    wList = [w[0]]
    stateList = [[n[0], m[0]]]
    fParticao = 0

    for i in range(1,len(w)):
        
        if w[i] not in wList:

            wList.append(w[i])
            chiSum.append((-1)*pnm[i]*pmn[i]*(np.exp(-val[int(n[i])]/T) - np.exp(-val[int(m[i])]/T)))
            stateList.append([n[i], m[i]])
            
        else:
            
            j = wList.index(w[i])
            chiSum[j] = chiSum[j] + (-1)*pnm[i]*pmn[i]*(np.exp(-val[int(n[i])]/T) - np.exp(-val[int(m[i])]/T))
            stateList[j].append(n[i])
            stateList[j].append(m[i])

    
    for n in range(len(val)):
        
        fParticao = fParticao + np.exp(-val[n]/T)
        
        
    wList, chiSum = (list(t) for t in zip(*sorted(zip(wList, chiSum))))
    
    chiSum = chiSum/fParticao
    
    return wList, chiSum, stateList, fParticao
    

def writeFile(w, T, chi, stateList, pasta):

    f = open(f"{pasta}/chiTempOutput/chiTemp-{w}.txt", "a")
    f.write('# T / chi\n')
    
    f_state_W = open(f'{pasta}/w_state/states-{w}.txt', 'a')
    f_state_W.write('# n / m\n')
    
    for j in range(len(T)):
        f.write(f'{T[j]} {chi[j]}\n')
    
    for i in range(0, len(stateList)-1, 1):
        f_state_W.write(f'{stateList[i]} {stateList[i+1]}\n')
    
    f.close()
    f_state_W.close()



### MAIN ###

N = 4
hop = '0.05'
pasta = f"../Dados_Hop/hopping-{hop}"

T = np.concatenate(( np.arange(0.1, 1, 0.01) , np.arange(1, 10, 0.1) ))

n, m, Pmn, Pnm, w = np.loadtxt(f"{pasta}/{N}_Pnm.txt", unpack=True)

val, vec = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")

chiT_list = []

fp = open(f"./{pasta}/Z.txt", "w")

for t in T:
    print(t)
    wList, chiSum, stateList, fParticao = soma(w, Pnm, Pmn, n, m, t)    
    
    fp.write(f'{t} {fParticao}\n')
    
    if(t == 0.1):
        for i in range(len(wList)):
            chiT_list.append([chiSum[i]])
    else:
        for i in range(len(wList)):
                chiT_list[i].append(chiSum[i])


chiListNew = []
wListNew = []
stateListNew = []

for i in range(len(chiT_list)):

    if wList[i] > 0:
        
        chiMax = max(chiT_list[i])
        chiMin = min(chiT_list[i])
        
        if chiMax > 0.0000000000001 or chiMin < -0.0000000000001:
        
            chiListNew.append(chiT_list[i])
            wListNew.append(wList[i])
            stateListNew.append(stateList[i])


for i in range(len(chiListNew)):
        
        writeFile(wListNew[i], T, chiListNew[i], stateListNew[i], pasta)

