import numpy as np
import matplotlib.pyplot as plt
import os


def Read_File_Matrix(file, dtype):
    
    
    with open(file, 'r') as f:
        
        lines = f.readlines()
        
        N = len(lines)
        
        if dtype == 'str':
            matrix = [['' for j in range(N)] for i in range(N)]
            
        elif dtype == 'int':
            matrix = np.zeros((N, N))
        
        for l in range(N):
            
            line = lines[l].strip("\n").split(',')
            
            for k in range(len(line)-1):
                
                matrix[l][k] = line[k]
    
    
    return matrix
    
    

num_estados = 256

hop = 1.0

pasta = f'../Dados_Hop/hopping-{hop}'

wList = np.loadtxt(f'../Classifica_chi/classificacao-hop{hop}.txt', usecols=0, unpack=True)
classificacao = np.loadtxt(f'../Classifica_chi/classificacao-hop{hop}.txt', usecols=1, dtype='str', unpack=True)

fileAnomalia = open(f'./superposicao_anomalia_{hop}.txt', 'w')
fileAnomalia.write(f'# w superposicao numero_estados_susceptibilidade formato ordem\n')

fileOutros = open(f'./superposicao_outros_{hop}.txt', 'w')
fileOutros.write(f'# w superposicao numero_estados_susceptibilidade formato ordem\n')


matriz_tt = Read_File_Matrix(f'{pasta}/operador_ciclo/matriz_teve_tunelamento.txt', 'int')
matriz_ordem = Read_File_Matrix(f'{pasta}/operador_ciclo/matriz_ordem.txt', 'int')
matriz_formato = Read_File_Matrix(f'{pasta}/operador_ciclo/matriz_formato.txt', 'str')
matriz_numero_conectados = Read_File_Matrix(f'{pasta}/operador_ciclo/matriz_numero_conectados.txt', 'int')

formato_dict = {"aberto":0, "fechado ordenado":1, "fechado desordenado":2}

for i, c in enumerate(classificacao):

    w = wList[i]
    
    print(w)
    
    nList = np.loadtxt(f'{pasta}/w_state/states-{w}.txt', unpack=True, ndmin=1, usecols=(0))
    mList = np.loadtxt(f'{pasta}/w_state/states-{w}.txt', unpack=True, ndmin=1, usecols=(1))

    ## Analise da superposicao
    superposicao = 0
    formato = np.zeros(3) # aberto, fechado ordenado, fechado desordenado
    ordem = np.zeros(8)
    numero_conectados = np.zeros(8)
        
    for i in range(len(nList)):
            
        n = int(nList[i])
        m = int(mList[i])
        
        if matriz_tt[n][m] == 1:
                
            superposicao = superposicao + 1
                
            formato[formato_dict[matriz_formato[n][m]]] = formato[formato_dict[matriz_formato[n][m]]] + 1
            
            o = int(matriz_ordem[n][m]) - 1
            ordem[o] = ordem[o] + 1
            
            nc = int(matriz_numero_conectados[n][m]) - 1
            numero_conectados[nc] = numero_conectados[nc] + 1
  
    
    if c == 'anomala':
        
        fileAnomalia.write(f'{w} {superposicao} {len(nList)}')
        
        for o in ordem:
            fileAnomalia.write(f' {o}')
        
        fileAnomalia.write('\n')
    
    else:

        fileOutros.write(f'{w} {superposicao} {len(nList)}')
        
        for o in ordem:
            fileOutros.write(f' {o}')
        
        fileOutros.write('\n')
    
        
        
fileAnomalia.close()
fileOutros.close()