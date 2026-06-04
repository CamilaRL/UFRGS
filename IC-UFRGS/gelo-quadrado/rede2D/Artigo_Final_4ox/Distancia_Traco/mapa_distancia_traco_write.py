import numpy as np

def read_autocoisas(filename):

    autovetor = []
    autovalor = []
    vetor = []
    i = 0

    with open(filename, "r") as f:
    
        lines = f.readlines()
        autocoisa = lines[0].strip("\n")
        
        for line in lines[1:]:
        
            line = line.strip("\n")
            
            if line == "Autovetores":
                autocoisa = line
            
            elif (autocoisa == "Autovetores") and (line != "Autovetores"):
                
                if(i==len(autovalor)):
                    autovetor.append(vetor)
                    i = 0
                    vetor = []
                    
                vetor.append(float(line))
                i = i + 1
            
            else:
                autovalor.append(float(line))
            
        autovetor.append(vetor)
        
    return autovalor, autovetor


def density_matrix(T, a, vetor):

    rho = np.exp(-a/T) * np.outer(vetor, vetor)
    
    Z = 0
    
    for i in range(len(rho)):
            
        Z = Z + rho[i][i]
        
    rho = rho/Z

    return rho
    
def distancia_traco(T, an, n, am, m):

    traco = 0

    rho_n = density_matrix(T, an, n)

    rho_m = density_matrix(T, am, m)

    rho_dif = np.zeros((len(rho_n), len(rho_n)))
    
    for i in range(len(rho_n)):
        for j in range(len(rho_n)):
            
            rho_dif[i][j] = rho_n[i][j] - rho_m[i][j]
    
    
    rho_dif = np.sqrt(rho_dif.conj().T * rho_dif)

    for i in range(len(n)):
    
        traco = traco + rho_dif[i][i]
        
    return traco/2
    


### Main ###

N = 4
t = 0.1
T = 0.1

pasta = f"../Dados_Hop/hopping-{t}"

val, vet = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")


f = open(f"{pasta}/mapa_traco_{t}_{T}.txt", "a")

for i in range(len(vet)):
    for j in range(len(vet)):
        
        print(f'{i} {j}')
        
        d = distancia_traco(T, val[i], vet[i], val[j], vet[j])

        f.write(f"{d} ")

    f.write("\n")

f.close()
