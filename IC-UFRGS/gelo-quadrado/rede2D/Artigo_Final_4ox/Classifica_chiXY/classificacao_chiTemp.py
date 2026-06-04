import numpy as np
import matplotlib.pyplot as plt
import math as m
import os


def Classifica(T, chiT):
    
    classes = ['finito', 'zero', 'anomala', 'NULL']
    c = 3
    
    chiMax = max(chiT)
    chiMin = min(chiT)
    
    for i in range(0, len(chiT)-1, 1):

        if (i > 2) and (i < len(chiT)-3) and (chiT[i] < chiT[i-1]) and (chiT[i] < chiT[i+1]) and (chiT[i] < chiT[i-3]) and (chiT[i] < chiT[i+3]):
        
            c = 2

        elif m.isclose(chiT[i], chiMax) and (T[i] < 1.0):
            
            c = 0
            
        elif m.isclose(chiT[i], chiMin) and (T[i] < 0.2):
            
            c = 1


    return classes[c]
    

def wList_Read(hop):
    
    path = f'../Dados_Hop/hopping-{hop}/w_state_xy/'
    wList = []
    
    for i in os.listdir(path):
        
        file = os.path.join(path, i)
        
        if os.path.isfile(file) and 'states-' in i:
            
            wList.append(float(i.replace(f'states-','').replace('.txt', '')))
            
    wList.sort()

    return wList


#### MAIN ####

N = 4
hop = 1.0

path = f"../Dados_Hop/hopping-{hop}/chiTempOutput_xy/"

wList = wList_Read(hop)

f = open(f"./classificacao-hop{hop}.txt", 'w')
f.write('# Frequencia / Classificacao\n')

for i in range(len(wList)):

    w = wList[i]
    
    filename = f'{path}/chiTemp-{w}.txt'
        
    T, chiT = np.loadtxt(filename, unpack=True)
        
    classe = Classifica(T, chiT)
    if classe=='anomala':
        print(f'w: {w}')
        
        plt.plot(T, chiT)
        plt.xlabel('Temperature')
        plt.ylabel('Imaginary Susceptibility')
        plt.title(f'w: {w}')
        plt.show()
    
    f.write(f'{w} {classe}\n')

f.close()