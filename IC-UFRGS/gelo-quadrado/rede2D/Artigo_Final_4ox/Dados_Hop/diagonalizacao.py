import numpy as np

N = 256
hop = '0.2'
pasta_matriz = f"./hopping-{hop}/4_hamiltoniano.txt"


### DIAGONALIZACAO

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


file_auto = open(f'./hopping-{hop}/4_autocoisas.txt', 'w')

file_auto.write('Autovalores\n')

for k in range(len(eigenvalues)):
    
    file_auto.write(f'{eigenvalues[k]}\n')

file_auto.write('Autovetores\n')

for j in range(len(eigenvalues)):
    
    for i in range(len(eigenvectors[0])):
        
        file_auto.write(f'{eigenvectors[j][i]}\n')




#### CALCULO DOS PESOS

file_pesosxx = f"./hopping-{hop}/4_Pxxnm.txt"
file_pesosxy = f"./hopping-{hop}/4_Pxynm.txt"
    
file_polarizacaoX = f"./hopping-{hop}/4_matriz_dipolo_X.txt"
file_polarizacaoY = f"./hopping-{hop}/4_matriz_dipolo_Y.txt"

fxx = open(file_pesosxx, "w")
fxy = open(file_pesosxy, "w")
    
PlistX = np.loadtxt(file_polarizacaoX, unpack=True)
PlistY = np.loadtxt(file_polarizacaoY, unpack=True)
 
Px = np.array(PlistX).reshape(N,N)
Py = np.array(PlistY).reshape(N,N)

for n in range(N):
    for m in range(N):
        
        wnm = eigenvalues[n] - eigenvalues[m]
        
        vn = eigenvectors[n]
        vm = eigenvectors[m]
        
        ## Pxx
        Pxnm = np.dot(vn, np.dot(Px, vm))
            
        Pxmn = np.dot(vm, np.dot(Px, vn))
            
        fxx.write(f"{n} {m} {Pxnm} {Pxmn} {wnm}\n")
            
        ## Pxy
        Pxnm = np.dot(vn, np.dot(Px, vm))
            
        Pymn = np.dot(vm, np.dot(Py, vn))
            
        fxy.write(f"{n} {m} {Pxnm} {Pymn} {wnm}\n")
        
fxx.close()
fxy.close()