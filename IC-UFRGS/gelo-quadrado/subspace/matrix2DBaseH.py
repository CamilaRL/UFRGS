import numpy as np
import copy as cp
import math as m
import itertools
import qutip as qt


## Base

def geradorCombinacoes():

    Narestas = Noxigenios*2
        
    combinacoesList = [list(p) for p in itertools.product([-1, 1], repeat=Narestas)]
    
    return combinacoesList


def hindex(x, y):
    
    return 1 + x%lado + lado * (y%lado)
    
def vindex(x, y):
    
    return lado**2 + 1 + lado * (x%lado) + y%lado


def Arestas_Oxigenio(i, j):
    
    direita = hindex(i,j) - 1
            
    esquerda = hindex(i-1,j) - 1
            
    cima = vindex(i,j) - 1
            
    baixo = vindex(i,j-1) - 1

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
    
    Narestas = 2*Noxigenios
    
    listaN = []
    
    for i in range(Narestas):
        
        if i == spinj:
            listaN.append(matriz)
        else:
            listaN.append(qt.qeye(2))
            
    matrizN = qt.tensor(listaN)
    
    return matrizN
    

def Hamiltoniano(J, hop):
    
    interacao = 0
    hx = 0
    
    Sz = qt.sigmaz()
    Sx = qt.sigmax()
    
    for oi in range(lado):
        
        for oj in range(lado):
            
            arestas = Arestas_Oxigenio(oi, oj)
            
            for a in range(4):
                for b in range(a+1, 4, 1):
                        
                    Sza = Operador(arestas[a], Sz)
                    Szb = Operador(arestas[b], Sz)
            
                    interacao = interacao + Sza * Szb
                    
    
    for k in range(2*Noxigenios):
        
        Sxk = Operador(k, Sx)
        
        hx = hx + Sxk
    

    H = (J/4) * interacao - hop * hx
    
    return H


def Plaqueta(i, j):

    baixo = hindex(i,j) - 1
    
    direita = vindex(i+1,j) - 1
            
    cima = hindex(i,j+1) - 1
            
    esquerda = vindex(i,j) - 1


    return baixo, direita, cima, esquerda
    
    
def Operador_Giro():

    plaqueta_giro = 0
    
    Sm = qt.sigmam()
    Sp = qt.sigmap()

    for i in range(lado):
        for j in range(lado):
            
            quadrado = Plaqueta(i, j)
            
            plaqueta_giro = plaqueta_giro + Operador(quadrado[0], Sm) * Operador(quadrado[1], Sm) * Operador(quadrado[2], Sp) * Operador(quadrado[3], Sp)
    
    Heff = - (plaqueta_giro + plaqueta_giro.dag())
    
    return Heff


def Traduz_Gelo_Completo(estado):
    
    ket = []
    
    for i in range(len(estado)):
    
        if estado[i] == 1:
            
            ket.append(qt.basis(2,0))
        
        else:
            
            ket.append(qt.basis(2,1))
            
    vetor = qt.tensor(ket)
    
    return vetor



def Hamiltoniano_Gelo(gelo_list, H_giro):
    
    size_gelo = len(gelo_list)
    
    H_reduzido = np.zeros((size_gelo, size_gelo))
    
    gelo_list_trad = []
    for gelo in gelo_list:
        
        gelo_list_trad.append(Traduz_Gelo_Completo(gelo))
        
    
    for i in range(size_gelo):
        for j in range(size_gelo):
    
            bra = qt.Qobj(gelo_list_trad[i]).dag()
            ket = qt.Qobj(gelo_list_trad[j])
            
            H_reduzido[i][j] = (bra * H_giro * ket).full()[0][0].real
            
    return H_reduzido
    
  
    
def dipole(estado):

    px = 0
    
    for i in range(lado):
        
        for j in range(lado):
               
            direita, esquerda, cima, baixo = Arestas_Oxigenio(i, j)
            
            px = px + estado[direita] + estado[esquerda]
            
    return px


### MAIN ###

global Noxigenios
global hop
global pasta

Noxigenios = 9
U = 10
hop = 1.0

pasta = f"./{Noxigenios}-hopping-{hop}"

global lado
lado = m.ceil(np.sqrt(Noxigenios))



estado_list = geradorCombinacoes()

gelo_list = []

for estado in estado_list:

    if Estados_Gelo(estado):
        gelo_list.append(estado)


#H = Hamiltoniano(U, hop)

H_giro = Operador_Giro()

H_gelo = Hamiltoniano_Gelo(gelo_list, H_giro)


############### TESTE
'''
vec = [1.0,1.0,1.0,1.0,-1.0,-1.0,-1.0,-1.0]
ket = []

for i in range(len(gelo_list[0])):
    
    if vec[i] == 1:
        
        ket.append(qt.basis(2,0))
    
    else:
        
        ket.append(qt.basis(2,1))
        
vetor = qt.tensor(ket)

vetor1 = Heff * vetor

vetor1_base = []

for i in range(0, 2*Noxigenios, 1):
    
    Szi = Operador(i, qt.sigmaz())
    
    vetor1_base.append((vetor1.dag() * Szi * vetor1).full()[0][0].real)
    
print(vec)
print(vetor1_base)
'''
    


Px = np.zeros((len(gelo_list), len(gelo_list)))

for i in range(len(gelo_list)):

    Px[i][i] = dipole(gelo_list[i])

print(Px)

## escrita de arquivos

## Estados Gelo
with open(f'{pasta}/{Noxigenios}_gelos.txt', 'w') as file:
    
    for estado in gelo_list:
        for e in estado:
                file.write(f'{e} ')
        
        file.write('\n')
               
    file.close()



## Hamiltoniano
with open(f'./{pasta}/{Noxigenios}_hamiltoniano.txt', 'w') as file:

    for i in range(len(H_gelo)):
        for j in H_gelo[i]:
            file.write(f'{j}\n')
            
    file.close()
 


## Matriz dipolo

with open(f'./{pasta}/{Noxigenios}_matriz_dipolo_X.txt', 'w') as file:

    for i in range(len(Px)):
        for j in Px[i]:
            file.write(f'{j}\n')
               
    file.close()