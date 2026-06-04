import numpy as np

N = 4
t = 0.021

pasta = f"./{N}oxigenios/hopping-{t}"

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


def diagonal_density_matrix(vetor):

    diagonal = []
    
    for i in range(len(vetor)):
        diagonal.append(vetor[i]*vetor[i])

    return np.array(diagonal)

def distancia_traco(n, m):

    traco = 0

    rho_n = diagonal_density_matrix(n)

    rho_m = diagonal_density_matrix(m)

    rho_dif = rho_n - rho_m
    
    rho_dif = np.sqrt(rho_dif*rho_dif)

    for i in range(len(n)):
    
        traco = traco + rho_dif[i]
        
    return traco/2
    


### Main ###

val, vet = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")


f = open(f"{pasta}/mapa_traco_{t}.txt", "a")

for i in range(len(vet)):
    for j in range(len(vet)):
    
        d = distancia_traco(vet[i], vet[j])

        f.write(f"{d} ")

    f.write("\n")

f.close()
