import numpy as np
import copy as cp
import math as m
import itertools


## Base

def geradorCombinacoes():

    Narestas = Noxigenios*2
        
    combinacoesList = [list(p) for p in itertools.product([1, 2], repeat=Narestas)]

    return combinacoesList


def BC(oxi):

    boundaryX_ox = []
    
    for i in range(lado):
    
        boundaryX_ox.append(lado - 1 + (i*lado))

    boundaryY_ox = []
    
    for i in range(lado):
    
        boundaryY_ox.append(Noxigenios - lado + i)


    if oxi not in boundaryX_ox:
        esquerda = 2*oxi
        direita = esquerda + 2
        
    elif oxi in boundaryX_ox:
        esquerda = 2*oxi
        direita = esquerda - 2*(lado-1)
    
    if oxi not in boundaryY_ox:
        cima = (2*oxi) + 1
        baixo = cima + 2*lado
        
    elif oxi in boundaryY_ox:
        cima = (2*oxi) + 1
        baixo = cima - 2*Noxigenios + 2*lado

    return cima, baixo, esquerda, direita


def baseOx(estado):

    estado_O = []

    for i in range(Noxigenios):
    
        cima, baixo, esquerda, direita = BC(i)
        
        oxi = [0,0]
        
        if estado[esquerda] == 1 and estado[direita] == 2:
            oxi[0] = 3
        elif estado[esquerda] == 1:
            oxi[0] = 1
        elif estado[direita] == 2:
            oxi[0] = 2
            
        if estado[cima] == 1 and estado[baixo] == 2:
            oxi[1] = 3
        elif estado[cima] == 1:
            oxi[1] = 1
        elif estado[baixo] == 2:
            oxi[1] = 2
            
        estado_O.append(oxi[0])
        estado_O.append(oxi[1])

    return estado_O


def energias(estadoH):
   
    sum = 0
    U = 1
    
    for e in range(Noxigenios):
    
        cima, baixo, esquerda, direita = BC(e)
        
        oxigenio = [estadoH[esquerda], estadoH[cima], estadoH[direita], estadoH[baixo]]
        
        
        for h in range(0, 3, 1):
            
            if oxigenio[h] == 1 and h < 2:
                i = 1
            
            elif oxigenio[h] == 2 and h == 2:
                i = 1
                
            else:
                i = 0
            
            for hh in range(h+1, 4, 1):
                    
                if hh == 1 and oxigenio[hh] == 1:
                
                    j = 1
                    sum = sum + U*(i - 0.5)*(j - 0.5)
                
                elif hh >= 2 and oxigenio[hh] == 2:
                    
                    j = 1
                    sum = sum + U*(i - 0.5)*(j - 0.5)
                    
                else:
                
                    j = 0
                    sum = sum + U*(i - 0.5)*(j - 0.5)
                      
    return sum
    
    
def hopping(braH, ketH):

    t = 0
    
    ccket = ketH.copy()
    
    for i in range(len(ketH)):
        
        if ccket[i] == 1:
            ccket[i] = 2
            
        elif ccket[i] == 2:
            ccket[i] = 1
        
        if np.array_equal(braH, ccket):
            t = 1
            break

        else:
            ccket = ketH.copy()
    
    return t


def matrizGerador(baseH):

    M = []
    Mlinha = []

    for bra in range(len(baseH)):
        for ket in range(len(baseH)):
            
            if (ket == bra):
                Mlinha.append(energias(baseH[ket]))
                
            else:
                Mlinha.append(-hop*hopping(baseH[bra], baseH[ket]))
                
        M.append(Mlinha)
        Mlinha = []
        
    return M
    
def dipole(estadoO):

    px = 0
    py = 0
    
    for i in range(0, len(estadoO)-1, 2):
        if estadoO[i] == 1:
            px = px - 1
        if estadoO[i+1] == 1:
            py = py + 1

        if estadoO[i] == 2:
            px = px + 1
        if estadoO[i+1] == 2:
            py = py - 1
    
    return (px**2 + py**2)**(1/2), px, py


### MAIN ###

global Noxigenios
global hop
global pasta

Noxigenios = 4
hop = 0.2
pasta = f"./hopping-{hop}"

global lado
lado = m.ceil(np.sqrt(Noxigenios))


estadoH_list = geradorCombinacoes()

estadoO_list = []
for estadoH in estadoH_list:

    estadoO_list.append(baseOx(estadoH))
    
    
H = matrizGerador(estadoH_list)


P = np.zeros((len(estadoO_list), len(estadoO_list)))
Px = np.zeros((len(estadoO_list), len(estadoO_list)))
Py = np.zeros((len(estadoO_list), len(estadoO_list)))

for i in range(len(estadoO_list)):

    P[i][i], Px[i][i], Py[i][i] = dipole(estadoO_list[i])



## escrita de arquivos

## Base H
with open(f'{pasta}/{Noxigenios}_baseH.txt', 'w') as file:
    
    for estado in estadoH_list:
        for e in estado:
                file.write(f'{e} ')
        
        file.write('\n')
               
    file.close()
    
    
## Base O
with open(f'{pasta}/{Noxigenios}_baseO.txt', 'w') as file:
    
    for estado in estadoO_list:
        for e in estado:
                file.write(f'{e} ')
        
        file.write('\n')
               
    file.close()


## Hamiltoniano
with open(f'./{pasta}/{Noxigenios}_hamiltoniano.txt', 'w') as file:

    for i in range(len(H)):
        for j in H[i]:
            file.write(f'{j}\n')
               
    file.close()
 


## Matriz dipolo
with open(f'./{pasta}/{Noxigenios}_matriz_dipolo.txt', 'w') as file:

    for i in range(len(P)):
        for j in P[i]:
            file.write(f'{j}\n')
               
    file.close()

with open(f'./{pasta}/{Noxigenios}_matriz_dipolo_X.txt', 'w') as file:

    for i in range(len(Px)):
        for j in Px[i]:
            file.write(f'{j}\n')
               
    file.close()
    
with open(f'./{pasta}/{Noxigenios}_matriz_dipolo_Y.txt', 'w') as file:

    for i in range(len(Py)):
        for j in Py[i]:
            file.write(f'{j}\n')
               
    file.close()