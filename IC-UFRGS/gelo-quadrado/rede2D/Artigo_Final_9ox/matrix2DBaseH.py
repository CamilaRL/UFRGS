import numpy as np
import copy as cp
import math as m
import itertools

global Noxigenios
global hop
global pasta

Noxigenios = 9
hop = 0.01
pasta = f"./{Noxigenios}oxigenios/hopping-{hop}"

global lado
lado = m.ceil(np.sqrt(Noxigenios))

## Base

def geradorCombinacoes():

    Narestas = Noxigenios*2
        
    combinacoesList = [list(p) for p in itertools.product([1, 2], repeat=Narestas)]

    return combinacoesList


def BC():

    boundaryXdir_ox = []
    boundaryXesq_ox = []
    
    for i in range(lado):
    
        boundaryXdir_ox.append(lado - 1 + (i*lado))
        boundaryXesq_ox.append(i*lado)

    boundaryYup_ox = []
    boundaryYdown_ox = []
    
    for i in range(lado):
    
        boundaryYup_ox.append(i)
        boundaryYdown_ox.append(Noxigenios - lado + i)

    return boundaryXdir_ox, boundaryXesq_ox, boundaryYup_ox, boundaryYdown_ox


def Vizinhos(oxi, boundaryXdir_ox, boundaryXesq_ox, boundaryYup_ox, boundaryYdown_ox):

    if oxi in boundaryXdir_ox:
        
        direita = oxi + 1 - lado
        esquerda = oxi - 1
        
    elif oxi not in boundaryXdir_ox:
        
        direita = oxi + 1

        if oxi in boundaryXesq_ox:
            esquerda = oxi + lado - 1
        else:
            esquerda = oxi - 1
    
    if oxi in boundaryYup_ox:

        cima = oxi + Noxigenios - lado
        baixo = oxi + lado

    elif oxi not in boundaryYup_ox:

        cima = oxi - lado

        if oxi in boundaryYdown_ox:
            baixo = oxi - Noxigenios + lado
        else:
            baixo = oxi + lado

    return cima, baixo, esquerda, direita


def baseOx(estado):

    estado_O = []
    boundaryXdir_ox, boundaryXesq_ox, boundaryYup_ox, boundaryYdown_ox = BC()

    for i in range(Noxigenios):
    
        cima, baixo, esquerda, direita = Vizinhos(i, boundaryXdir_ox, boundaryXesq_ox, boundaryYup_ox, boundaryYdown_ox)
        
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


def Energias(estadoH):

    print('Energias')

    sum = 0
    U = 1
    
    boundaryXdir_ox, boundaryXesq_ox, boundaryYup_ox, boundaryYdown_ox = BC()
    
    for e in range(Noxigenios):
    
        cima, baixo, esquerda, direita = Vizinhos(e, boundaryXdir_ox, boundaryXesq_ox, boundaryYup_ox, boundaryYdown_ox)
        
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
    
    
def Hopping(braH, ketH):
    
    t = 0
    
    counter_dif = 0
    
    for i in range(len(ketH)):
        
        if ketH[i] != braH[i]:
            counter_dif = counter_dif + 1
    
    if counter_dif == 1:
        t = 1
    
    return t


def matrizGerador(baseH):

    M = []
    Mlinha = []

    for bra in range(len(baseH)):
        for ket in range(len(baseH)):
            
            if (ket == bra):
                Mlinha.append(Energias(baseH[ket]))
                
            else:
                print(f'Hopping: {bra} {ket}')
                Mlinha.append(-hop*Hopping(baseH[bra], baseH[ket]))
                
        M.append(Mlinha)
        Mlinha = []
        
    return M


def dipole(estadoO):

    print('Dipolo')

    px = 0
    py = 0
    
    for i in range(len(estadoO)-1):
        if estadoO[i] == 1:
            px = px + 1
        if estadoO[i+1] == 1:
            py = py + 1

        if estadoO[i] == 2:
            px = px - 1
        if estadoO[i+1] == 2:
            py = py - 1
    
    return (px**2 + py**2)**(1/2), px, py


### MAIN ###

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
print('Escrita de Arquivos')

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