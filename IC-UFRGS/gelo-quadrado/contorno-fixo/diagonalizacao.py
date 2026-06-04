import numpy as np

Noxigenios = 9
hop = '0.1'
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




fxx = open(f"./{Noxigenios}-hopping-{hop}/{Noxigenios}_Pxxnm.txt", "w")
    
PlistX = np.loadtxt(f"./{Noxigenios}-hopping-{hop}/{Noxigenios}_matriz_dipolo_X.txt", unpack=True)


for n in range(N):
    
    vn = eigenvectors[n]
    
    vn_novo = []
    indexes = []
    
    for i in range(N):
    
        if vn[i] > 1e-6:
            vn_novo.append(vn[i])
            indexes.append(i)

    if len(indexes) > 0:
        
        for m in range(n+1, N, 1):
            
            vm_novo = []
        
            vm = eigenvectors[m]
            
            Pxvn = np.zeros(len(vn_novo))
            
            ## Pxx
            
            for i, v in enumerate(indexes):
                
                Pxvn[i] = PlistX[v] * vn_novo[i]
                
                vm_novo.append(vm[v])
            
            Pxmn = np.dot(vm_novo, Pxvn)
            

            if abs(Pxmn) > 1e-5:
                
                print(n, m, Pxmn)
                
                wmn = eigenvalues[m] - eigenvalues[n]
            
                fxx.write(f"{n} {m} {Pxmn} {wmn}\n")


fxx.close()