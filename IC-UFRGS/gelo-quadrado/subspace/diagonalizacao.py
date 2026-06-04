import numpy as np

Noxigenios = 9
hop = '1.0'
pasta_matriz = f"./{Noxigenios}-hopping-{hop}/{Noxigenios}_hamiltoniano.txt"


### DIAGONALIZACAO

with open(f'./{Noxigenios}-hopping-{hop}/{Noxigenios}_gelos.txt', 'r') as f:
    
    linhas = f.readlines()
    N = len(linhas)


Hlist = np.loadtxt(pasta_matriz, unpack=True)

H = np.array(Hlist).reshape(N,N)

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


file_auto = open(f'./{Noxigenios}-hopping-{hop}/{Noxigenios}_autocoisas.txt', 'w')

file_auto.write('Autovalores\n')

for k in range(len(eigenvalues)):
    
    file_auto.write(f'{eigenvalues[k]}\n')

file_auto.write('Autovetores\n')

for j in range(len(eigenvalues)):
    
    for i in range(len(eigenvectors[0])):
        
        file_auto.write(f'{eigenvectors[j][i]}\n')




#### CALCULO DOS PESOS

file_pesosxx = f"./{Noxigenios}-hopping-{hop}/{Noxigenios}_Pxxnm.txt"
    
file_polarizacaoX = f"./{Noxigenios}-hopping-{hop}/{Noxigenios}_matriz_dipolo_X.txt"

fxx = open(file_pesosxx, "w")
    
PlistX = np.loadtxt(file_polarizacaoX, unpack=True)

Px = np.array(PlistX).reshape(N,N)

for n in range(N):
    for m in range(N):
        
        wnm = eigenvalues[n] - eigenvalues[m]
        
        vn = eigenvectors[n]
        vm = eigenvectors[m]
        
        ## Pxx
        Pxnm = np.dot(vn, np.dot(Px, vm))
        
        Pxmn = np.dot(vm, np.dot(Px, vn))
        
        fxx.write(f"{n} {m} {Pxnm} {Pxmn} {wnm}\n")


fxx.close()