import numpy as np
import matplotlib.pyplot as plt
from qutip import *
import itertools
import os


def geradorCombinacoes(Noxigenios):

    himparList = [list(p) for p in itertools.product([0, 1], repeat=Noxigenios)]
    
    combinacoesList = []
    
    for himpar in himparList:
        
        estado = []
        
        for i in range(Noxigenios):
            
            nimpar = himpar[i]
            npar = 1 - nimpar
            
            estado.append(nimpar)
            estado.append(npar)
            
        combinacoesList.append(estado)
    
    return himparList, combinacoesList


def Energia_Hex(Noxigenios, estado):
    
    E = -0.5 * Noxigenios
    
    for i in range(1, len(estado), 2):
       
        if i == len(estado)-1:
            j = 0
        else:
            j = i+1
        
        E =  E + 2*estado[i]*estado[j]
        
    return E
    
    
def Hopping_Hex(estado_i, estado_j):
    
    tem_hop = 0
    
    for k in range(len(estado_i)):
        
        if estado_i[k] != estado_j[k]:
            
            tem_hop = tem_hop + 1
            
    if tem_hop != 1:
        
        tem_hop = 0
    
    return tem_hop


def Phonon(H, Px, Py, num_bosons, w, delta_x, delta_y):
    
    g = -1
    
    b_d = destroy(num_bosons)
    b_c = create(num_bosons)

    H_ph = w * b_c * b_d
    
    H_I = g*tensor(Px, (b_d + b_c)) + g*tensor(Py, (b_d + b_c))
    
    H_total = tensor(H, qeye(num_bosons)) + tensor(qeye(64), H_ph) + H_I
    
    Px_total = tensor(Px, qeye(num_bosons)) + delta_x * tensor(qeye(64), (b_d + b_c))
    
    Py_total = tensor(Py, qeye(num_bosons)) + delta_y * tensor(qeye(64), (b_d + b_c))
    
    return H_total.full(), np.real(Px_total.full()), np.real(Py_total.full())
    

def Diagonalizacao(H):
    
    eigenvalues_complex, eigenvectors_complex = np.linalg.eig(H)

    eigenvalues = []
    eigenvectors = []

    for k in range(len(eigenvalues_complex)):
        
        eigenvalues.append(eigenvalues_complex[k].real)

        vec = []

        for i in range(len(eigenvectors_complex[0])):
            
            vec.append(eigenvectors_complex[i][k].real)
            
        eigenvectors.append(vec)

    eigenvalues, eigenvectors = (list(t) for t in zip(*sorted(zip(eigenvalues, eigenvectors))))
    
    return eigenvalues, eigenvectors
    


def Polarizacao(n):
    
    theta = np.pi/6
    
    cos = np.cos(theta)
    sin = np.sin(theta)
    
    Px0 = n[0]*cos - n[-1]*cos
    Py0 = n[0]*sin + n[-1]*sin - 1
    
    Px1 = cos - n[1]*cos
    Py1 = n[2] - n[1]*sin - sin
    
    Px2 = -n[4]*cos + cos
    Py2 = -n[3] + n[4]*sin + sin
    
    Px3 = n[5]*cos - n[6]*cos
    Py3 = -n[5]*sin - n[6]*sin + 1
    
    Px4 = n[7]*cos - cos
    Py4 = n[7]*sin - n[8] + sin
    
    Px5 = n[10]*cos - cos
    Py5 = n[9] - n[10]*sin - sin
    
    Px = Px0 + Px1 + Px2 + Px3 + Px4 + Px5
    Py = Py0 + Py1 + Py2 + Py3 + Py4 + Py5
    
    return Px, Py


def Pesos(N, eigenvalues, eigenvectors, Px, Py):
    
    fp = open(f'./hopping-{t}/{N}_Pnm.txt', "w")
    
    for n in range(N):
        for m in range(N):
            
            wnm = eigenvalues[n] - eigenvalues[m]
            
            vn = eigenvectors[n]
            vm = eigenvectors[m]
            
            ## Pxx
            Pxnm = np.dot(vn, np.dot(Px, vm))
            
            Pxmn = np.dot(vm, np.dot(Px, vn))
            
            Pynm = np.dot(vn, np.dot(Py, vm))
            
            Pymn = np.dot(vm, np.dot(Py, vn))
            
            fp.write(f"{n} {m} {Pxnm} {Pxmn} {Pymn} {Pynm} {wnm:.5f}\n")
            
    fp.close()
    

### MAIN ###

Noxigenios = 6
U = 1
t = 0.5

num_bosons = 5
w_bosons = 1
dx = 0
dy = 0

#os.mkdir(f'./hopping-{t}/')

print('Gerador de Combinacoes')
himparList, htodosList = geradorCombinacoes(Noxigenios)


print('Hamiltoniano')
H = np.zeros((len(himparList), len(himparList)))

for i, estado in enumerate(htodosList):
    
    E = Energia_Hex(Noxigenios, estado)

    H[i][i] = E*U

    for j in range(i+1, len(himparList)):
        
        h = Hopping_Hex(himparList[i], himparList[j])

        H[i][j] = -h*t
        H[j][i] = -h*t


print('Matriz de Polarizacao')
Px_matrix = np.zeros((len(himparList), len(himparList)))
Py_matrix = np.zeros((len(himparList), len(himparList)))

for i in range(len(htodosList)):
    
    Px, Py = Polarizacao(htodosList[i])
    
    Px_matrix[i][i] = Px
    Py_matrix[i][i] = Py


print('Phonons')
H_total, Px_total, Py_total = Phonon(Qobj(H), Qobj(Px_matrix), Qobj(Py_matrix), num_bosons, w_bosons, dx, dy)


print('Diagonalizacao')
evals, evecs = Diagonalizacao(H_total)

fauto = open(f'./hopping-{t}/{Noxigenios}_autocoisas.txt', 'w')

fauto.write('Autovalores\n')

for k in range(len(evals)):
    
    fauto.write(f'{evals[k]}\n')

fauto.write('Autovetores\n')

for j in range(len(evals)):
    
    for i in range(len(evecs[0])):
        
        fauto.write(f'{evecs[j][i]}\n')
        
fauto.close()


print('Pesos') 
Pesos(Noxigenios, evals, evecs, Px_total, Py_total)