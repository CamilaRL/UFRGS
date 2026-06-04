import numpy as np
import copy as cp
import math as m
import itertools
import qutip as qt
import matplotlib.pyplot as plt


## Base

def geradorCombinacoes(contorno):
    
    arestasContorno = [0, 1, 2, 9, 10, 11, 12, 15, 16, 19, 20, 23]
    
    Narestas = 24
    NarestasVariaveis = 12
    
    configVariaveis = [list(p) for p in itertools.product([-1, 1], repeat=NarestasVariaveis)]
    
    combinacoesList = []
    
    for variavel in configVariaveis:
        
        lista = np.zeros(Narestas)
        
        c = 0
        v = 0
        
        for i in range(Narestas):
            
            if i in arestasContorno:
                
                lista[i] = contorno[c]
                c = c + 1
            
            else:
                
                lista[i] = variavel[v]
                v = v + 1
            
        
        combinacoesList.append(lista)
    
    return combinacoesList


def hindex(x, y):
    
    return 12 + y + 4*x
    
def vindex(x, y):
    
    return y + x*lado


def Arestas_Oxigenio(i, j):
    
    direita = hindex(i,j+1)
            
    esquerda = hindex(i,j)
            
    cima = vindex(i,j+3)
            
    baixo = vindex(i,j)

    return direita, esquerda, cima, baixo


def Estados_Gelo(estado):

    soma = []
    estados_gelo_list = []

    for i in range(lado):
        
        for j in range(lado):
               
            direita, esquerda, cima, baixo = Arestas_Oxigenio(i, j)
            
            soma.append( abs(estado[direita] - estado[esquerda] + estado[cima] - estado[baixo]) )
            
    if sum(soma) == 0:
        return True ## é estado de gelo
    else:
        return False


def Operador(spinj, matriz):
    
    Narestas = 24
    
    listaN = []
    
    for i in range(Narestas):
        
        if i == spinj:
            listaN.append(matriz)
        else:
            listaN.append(qt.qeye(2))
            
    matrizN = qt.tensor(listaN)
    
    return matrizN
    

def Hamiltoniano(J, hop, estado_list):
    
    N = len(estado_list)
    H = np.zeros((N, N))
    
    for i, estado_i in enumerate(estado_list):
        
        E = 0
        
        for oi in range(3):
            for oj in range(3):
                
                aresta = Arestas_Oxigenio(oi, oj)
                
                for a in range(4):
                    for b in range(a+1, 4, 1):
                        
                        E = E + estado_i[aresta[a]] * estado_i[aresta[b]]
        
        H[i][i] = E*J/4
    
    
        for j in range(i+1, N, 1):

            if np.linalg.norm(estado_i - estado_list[j]) == 2:
                
                H[i][j] = -hop
                H[j][i] = -hop
            
    return H
  
    
def dipole(estado):

    px = 0
    
    for i in range(lado):
        
        for j in range(lado):
               
            direita, esquerda, cima, baixo = Arestas_Oxigenio(i, j)
            
            px = px + (estado[direita] + estado[esquerda])*0.5
            
    return px


### MAIN ###

global Noxigenios
global hop
global pasta

Noxigenios = 9
U = 1
hop = 0.1

pasta = f"./{Noxigenios}-hopping-{hop}"

global lado
lado = m.ceil(np.sqrt(Noxigenios))


contorno = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1]

estado_list = geradorCombinacoes(contorno)


H = Hamiltoniano(U, hop, estado_list)


Px = np.zeros((len(estado_list), len(estado_list)))

for i in range(len(estado_list)):

    Px[i][i] = dipole(estado_list[i])



## escrita de arquivos

## Estados Gelo
with open(f'{pasta}/{Noxigenios}_gelos.txt', 'w') as file:
    
    for estado in estado_list:
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

with open(f'./{pasta}/{Noxigenios}_matriz_dipolo_X.txt', 'w') as file:

    for i in range(len(Px)):
        for j in Px[i]:
            file.write(f'{j}\n')
               
    file.close()