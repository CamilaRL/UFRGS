import numpy as np
import matplotlib.pyplot as plt
import os

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

def read_base(filename):
    base = []
    vetor_ox = []
    vetor_rede = []

    with open(filename, 'r') as f:
        
        lines = f.readlines()
        
        for line in lines:
            line = line.strip(' \n').split(' ')
            line = [float(l) for l in line]
     
            if len(line) > 1:
            
                for i in range(len(line)):
                
                    vetor_ox.append(line[i])

                    if len(vetor_ox) == 2:
                        vetor_rede.append(vetor_ox)
                        vetor_ox = []
                        
            
                base.append(line)
            
    return base


def base_h(estado):

    h = np.zeros(len(estado))
    
    for i in range(len(estado)):
        
        e = estado[i]
        
        if e == 0:
            h[i] = 2
        if e == 1:
            h[i] = 1
        if e == 2:
            h[i] = 2
        if e == 3:
            h[i] = 1
            
    return h

def quadrado_read(hn, i):
    
    hcima = hn[i]

    if (i == 0):
            
        hbaixo = hn[i+N]
                
        vesq = hn[i+2*N-1]
                 
        vdir = hn[i+1+N]

    elif (i >= N):
            
        hbaixo = hn[i-N]
            
        vdir = hn[i-N+1]

        if (i >= (N+2)):
            vesq = hn[i-N-1]
        else:
            vesq = hn[i-1]

    else:
    
        hbaixo = hn[i+N]
        
        vesq = hn[i-1+N]
        
        vdir = hn[i+1+N]
        
    return hcima, hbaixo, vdir, vesq

def quadrado_save(hn, i, hcima, hbaixo, vdir, vesq):

    hn[i] = hcima

    if (i == 0):
            
        hn[i+N] = hbaixo
                
        hn[i+2*N-1] = vesq
                 
        hn[i+1+N] = vdir

    elif (i >= N):
            
        hn[i-N] = hbaixo
            
        hn[i-N+1] = vdir

        if (i >= (N+2)):
            hn[i-N-1] = vesq
        else:
            hn[i-1] = vesq

    else:
        hn[i+N] = hbaixo
        
        hn[i-1+N] = vesq
        
        hn[i+1+N] = vdir
        
    return hn

def operador_ciclo(hn, estados_base):
    
    #horario = 0
    #antihorario = 0
    
    hn_list = []

    ## Testa se consegue girar um quadrado inteiro. Se consegue, ele salva o novo estado
    for i in range(0, 2*N, 2):
        
        hcima1, hbaixo1, vdir1, vesq1 = quadrado_read(hn, i)

        if (hcima1 == vdir1) and (hbaixo1 == vesq1):
                    
            hn_novo = hn.copy()
            
            if (hcima1 == 2) and (hbaixo1 == 1):
                #horario = horario + 1

                hn_novo = quadrado_save(hn_novo, i, 1, 2, 1, 2)                

                for i, estado in enumerate(estados_base):
                    if np.array_equal(estado, hn_novo):  # Comparação de listas
                        b = i
                        break
                        
                hn_list.append(b)
                
            elif (hcima1 == 1) and (hbaixo1 == 2):                
                #antihorario = antihorario + 1
                
                hn_novo = quadrado_save(hn_novo, i, 2, 1, 2, 1)
                
                for i, estado in enumerate(estados_base):
                    if np.array_equal(estado, hn_novo):  # Comparação de listas
                        b = i
                        break

                hn_list.append(b)

    return hn_list


def Frequency_From_Folder(folder):
    
    path = folder + '/w_state/'
    
    files = []
    wList = []
    stateList = []

    for i in os.listdir(path):

        if os.path.isfile(os.path.join(path,i)) and 'states-' in i:
        
            files.append(i)
            wList.append(float(i.replace(f'states-','').replace('.txt', '')))

    wList, files = (list(t) for t in zip(*sorted(zip(wList, files))))
    
    
    for file in files:
        
        List = []
        n = np.loadtxt(path+file, unpack=True, usecols=(0), ndmin=1)
        m = np.loadtxt(path+file, unpack=True, usecols=(1), ndmin=1)
        
        for i in range(len(n)):
            
            List.append(int(n[i]))
            List.append(int(m[i]))
        
        stateList.append(List)
    
    return wList, stateList


def Arquivo_Saida(f, matriz):

    for t in range(len(matriz)):
        for tt in range(len(matriz[t])):
        
            f.write(f'{matriz[t][tt]} ')
        
        f.write('\n')
    
    f.close()
    

def Operador_Ciclo(N, hop):

    
    pasta = f"../Dados_Hop/hopping-{hop}"
    
    fileOut = open(f'{pasta}/NumeroCiclos.txt', 'w')
    
    wList, stateList = Frequency_From_Folder(pasta)
    
    estados_base_h = read_base(f'{pasta}/{N}_baseH.txt')
    
    val, vet = read_autocoisas(f"{pasta}/{N}_autocoisas.txt")
    
    operador_base = []

    ## aplica o operador 1 ciclio nos estados da base
    for he in estados_base_h:
        hn_list = operador_ciclo(he, estados_base_h)
        
        operador_base.append(hn_list)
    
    for w in wList:
        
        fileMatriz = open(f'{pasta}/operador_ciclo/{w}.txt', 'w')
        
        TemCiclos = 0
            
        print(w)
        prob_matrix = np.zeros((len(vet), len(vet)))
        tem_ciclos = np.zeros((len(vet), len(vet)))

        k = wList.index(w)

        nm = stateList[k]

        transicoes_list = [[] for j in range(int(max(nm))+1)]

        for j in range(0, len(nm), 2):
                    
            transicoes_list[int(nm[j])].append(int(nm[j+1]))

        for t in range(len(transicoes_list)):

            vet1 = vet[t]
            vet1_operado = np.zeros(len(vet1))
            
            for i in range(len(operador_base)):
                for j in range(len(operador_base[i])):

                    ## para mapa dos valores esperados
                    vet1_operado[operador_base[i][j]] = vet1_operado[operador_base[i][j]] + vet1[i]
                         
                            
            for tt in transicoes_list[t]:
                        
                val_esperado = 0
                vet2 = vet[tt]
                        
                for i in range(len(vet2)):
                    val_esperado = val_esperado + vet2[i]*vet1_operado[i]
                        
                prob_matrix[t][tt] = prob_matrix[t][tt] + val_esperado*val_esperado
                        
                if val_esperado*val_esperado > 0:
                    tem_ciclos[t][tt] = 1
                    TemCiclos = TemCiclos + 1
                        
        fileOut.write(f'{w} {TemCiclos}\n')
        Arquivo_Saida(fileMatriz, tem_ciclos)
        fileMatriz.close()


### MAIN ###

N = 4
hop = 0.001

Operador_Ciclo(N, hop)