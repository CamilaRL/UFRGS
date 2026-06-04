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
    

def pesos(val, vet):

    file_pesos = f"../Dados_Hop/hopping-{hop}/{nO}_Pnm.txt"
    file_pesosxx = f"../Dados_Hop/hopping-{hop}/{nO}_Pxxnm.txt"
    file_pesosxy = f"../Dados_Hop/hopping-{hop}/{nO}_Pxynm.txt"
    
    file_polarizacao = f"../Dados_Hop/hopping-{hop}/{nO}_matriz_dipolo.txt"
    file_polarizacaoX = f"../Dados_Hop/hopping-{hop}/{nO}_matriz_dipolo_X.txt"
    file_polarizacaoY = f"../Dados_Hop/hopping-{hop}/{nO}_matriz_dipolo_Y.txt"
    
    f = open(file_pesos, "w")
    fxx = open(file_pesosxx, "w")
    fxy = open(file_pesosxy, "w")
    
    Plist = np.loadtxt(file_polarizacao, unpack=True)
    PlistX = np.loadtxt(file_polarizacaoX, unpack=True)
    PlistY = np.loadtxt(file_polarizacaoY, unpack=True)
 
    P = np.array(Plist).reshape(N,N)
    Px = np.array(PlistX).reshape(N,N)
    Py = np.array(PlistY).reshape(N,N)
    
    for n in range(N):
        for m in range(N):
        
            wnm = val[n] - val[m]
            
            vn = np.array(vet[n])
            vm = np.array(vet[m])
            
            ## P
            Pnm = np.dot(vn, np.dot(P,vm))
            
            Pmn = np.dot(vm, np.dot(P,vn))
            
            f.write(f"{n} {m} {Pnm} {Pmn} {wnm}\n")
            
            ## Pxx
            Pxnm = np.dot(vn, np.dot(Px, vm))
            
            Pxmn = np.dot(vm, np.dot(Px, vn))
            
            fxx.write(f"{n} {m} {Pxnm} {Pxmn} {wnm}\n")
            
            ## Pxy
            Pxnm = np.dot(vn, np.dot(Px, vm))
            
            Pymn = np.dot(vm, np.dot(Py, vn))
            
            fxy.write(f"{n} {m} {Pxnm} {Pymn} {wnm}\n")
            

    f.close()
    fxx.close()
    fxy.close()
 
# MAIN #

N = 256
nO = 4
hop = 1.0


val, vet = read_autocoisas(f"../Dados_Hop/hopping-{hop}/{nO}_autocoisas.txt")

pesos(val, vet)