import numpy as np
import os


def wList_Read(hop):
    
    path = f'../Dados_Hop/hopping-{hop}/w_state/'
    wList = []
    
    for i in os.listdir(path):
        
        file = os.path.join(path, i)
        
        nList = np.loadtxt(file, unpack=True, usecols=(1), ndmin=1)
        
        if len(nList) > 1:
            
            if os.path.isfile(file) and 'states-' in i:
            
                wList.append(float(i.replace(f'states-','').replace('.txt', '')))
                
    return wList


### Main ###

hop = 0.1

wList = wList_Read(hop)

for w in wList:

    print(w)

print(len(wList))