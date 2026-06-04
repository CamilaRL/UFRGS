import numpy as np
import matplotlib.pyplot as plt
import math

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


def Polarizacao(estado):
    
    px = 0
    py = 0
    
    for i in range(0, len(estado)-1, 2):
        
        if estado[i] == 1:
            px = px - 1
            
        if estado[i+1] == 1:
            py = py + 1

        if estado[i] == 2:
            px = px + 1
            
        if estado[i+1] == 2:
            py = py - 1
    
    return [px, py]


def Vizinhaça_RedeEscada(h, Nox):
    
    lado_y = 2
    lado_x = int(Nox/lado_y)
    
    paridade = h%2
    
    vizinhos = []
    
    ## se for na par = esta em x
    if paridade == 0:
    
        direita = h + 2
        esquerda = h - 2
        cima_direita = h + 1
        cima_esquerda = h - 1
        baixo_direita = h + Nox + 1
        baixo_esquerda = h + Nox - 1
        
        if h%(Nox) == 0 :
            
            esquerda = h + 2*(lado_x - 1)
            cima_esquerda = h + lado_x + 1
            
            if h == 0:
                
                baixo_esquerda = 2*Nox - 1
                
        if h >= Nox:
            
            baixo_direita = h - Nox + 1
            baixo_esquerda = baixo_direita - 2
            
            if h == Nox:
                   
                baixo_esquerda = h - 1
        
        if h == 2*(lado_x - 1) or h == (2*Nox - 2):
            
            direita = h - (Nox - 2)
        
        
        vizinhos = [esquerda, cima_esquerda, baixo_esquerda, direita, cima_direita, baixo_direita]
        
    ## se for impar = esta em y
    elif paridade != 0:
        
        if h < Nox:
            
            cima = h + Nox
            baixo = h + Nox
            cima_direita = h + Nox + 1
            cima_esquerda = h + Nox - 1
            baixo_direita = h + 1
            baixo_esquerda = h - 1
            
            if h == (Nox - 1):
                
                cima_direita = Nox
                baixo_direita = 0
        
        if h >= Nox:
            
            cima = h - Nox
            baixo = h - Nox
            cima_direita = h - Nox + 1
            cima_esquerda = h - Nox - 1
            baixo_direita = h + 1
            baixo_esquerda = h - 1
            
            if h == (2*Nox - 1):
                
                cima_direita = 0
                baixo_direita = Nox
        
        
        vizinhos = [cima, cima_esquerda, baixo_esquerda, baixo, cima_direita, baixo_direita]
        
    return paridade, vizinhos


def Vertice(aresta):

    vertices = [[0,1,2,5], [2,3,0,7], [4,5,6,1], [6,7,4,3]] ## [esquerda, cima, direita, baixo]
    
    vertice_aresta = []
    pos_vertice = [] ## [esquerda = 0, cima = 1, direita = 2, baixo = 3]
    
    for v in range(len(vertices)):
        
        if aresta in vertices[v]:
            
            pos = vertices[v].index(aresta)
            
            vertice_aresta.append(v)

            pos_vertice.append(pos)
            
    return vertice_aresta, pos_vertice



def Classifica_Tunelamento_Coletivo(conexao, estado_i, estado_f):
    
    formato = 'nada'    
    setas = []
    setas_vertices_partidas = []
    setas_vertices_chegadas = []
    
    for aresta in conexao:
            
        vertices_aresta, pos_vertice = Vertice(aresta)
        
        seta = estado_i[aresta] - estado_f[aresta]

        setas.append(seta)
       
        if seta < 0:
            
            if aresta%2 == 0:
                
                partida = pos_vertice.index(0) ## esquerda
                chegada = pos_vertice.index(2) ## direita
            
            else:
                
                partida = pos_vertice.index(1) ## cima
                chegada = pos_vertice.index(3) ## baixo
    
        if seta > 0:
            
            if aresta%2 == 0:
                
                partida = pos_vertice.index(2) ## direita
                chegada = pos_vertice.index(0) ## esquerda
            
            else:
                
                partida = pos_vertice.index(3) ## baixo
                chegada = pos_vertice.index(1) ## cima
        
        setas_vertices_partidas.append(vertices_aresta[partida])
        setas_vertices_chegadas.append(vertices_aresta[chegada])
    
    fechado = True
    ordem = len(conexao)

    for v in range(4):
        
        c = setas_vertices_chegadas.count(v)
        p = setas_vertices_partidas.count(v)
        
        if c%2 == 0 and c > 0:
            ordem = ordem - 1 
        
        if c == 1 and p == 1:
            
            fechado = fechado and True
        
        else:
            
            fechado = fechado and False
    
    
    if fechado:
        
        formato = 'fechado'
        
        if sum(setas) == 0:
        
            formato = formato + ' ordenado'
        
        else:
        
            formato = formato + ' desordenado'
            
    else:
        
        formato = 'aberto'
        
    return formato, ordem
    


def Tunelamento_Coletivo(estado_i, estado_f, vizinhanca_rede):
    
    teve_tunelamento = 0
    
    h_diferentes = []
    
    for h in range(len(estado_i)):
        
        if estado_i[h] != estado_f[h]:
            
            h_diferentes.append(h)
    
    
    conexao = [h_diferentes[0]]
    numero_conexoes_h = []
    
    for h1 in conexao:
        
        soma = 0
        
        for h2 in h_diferentes:
            
            if h2 in vizinhanca_rede[h1]:
            
                soma = soma + 1
                
                if h2 not in conexao:
                
                    conexao.append(h2)
        
        numero_conexoes_h.append(soma)
    
    if len(conexao) == len(h_diferentes):
        teve_tunelamento = 1

    return teve_tunelamento, len(conexao), conexao


def Estados_Tunelados(base_H, polarizacao_base, estados_mesma_polarizacao, vizinhanca_rede):
    
    matriz_teve_tunelamento = np.zeros((len(base_H), len(base_H)))
    
    matriz_ordem = np.zeros((len(base_H), len(base_H)))
    
    matriz_formato = [ ['' for i in range(len(base_H))] for i in range(len(base_H))]

    matriz_numero_conectados = np.zeros((len(base_H), len(base_H)))
    
    
    
    for p, polarizacao_estado in enumerate(polarizacao_base):
        
        for ei in estados_mesma_polarizacao[p]:
            
            for ef in estados_mesma_polarizacao[p]:
            
                if ei != ef:
                    
                    print(f'{ei} {ef}')
                    
                    teve_tunelamento, numero_conectados, conexao = Tunelamento_Coletivo(base_H[ei], base_H[ef], vizinhanca_rede)
                    
                    formato, ordem = Classifica_Tunelamento_Coletivo(conexao, base_H[ei], base_H[ef])
                    
                    matriz_teve_tunelamento[ei][ef] = teve_tunelamento
                    matriz_numero_conectados[ei][ef] = numero_conectados
                    matriz_ordem[ei][ef] = ordem
                    matriz_formato[ei][ef] = formato

    return matriz_teve_tunelamento, matriz_numero_conectados, matriz_ordem, matriz_formato


def Write_File(path, matriz):
    
    f = open(path, 'w')
    
    for i in range(len(matriz)):
        for j in range(len(matriz)):
            
            f.write(f'{matriz[i][j]},')
         
        f.write('\n')
        
    f.close()
    
    

### MAIN ###


## parametros

Nox = 4
hop = 1.0
pasta = f'../Dados_Hop/hopping-{hop}'


## leitura arquivos

base_H = read_base(f'{pasta}/{Nox}_baseH.txt')

autoval, autovet = read_autocoisas(f'{pasta}/{Nox}_autocoisas.txt')


## constroi vizinhanca da rede

vizinhanca_rede = []
paridade_rede = []

for h in range(0, (2*Nox), 1):
    
    paridade, vizinhos = Vizinhaça_RedeEscada(h, Nox)

    vizinhanca_rede.append(vizinhos)
    paridade_rede.append(paridade)


## polarizacao

polarizacao_base = []
estados_mesma_polarizacao = []

for i in range(len(base_H)):
    
    polarizacao_estado = Polarizacao(base_H[i])
    
    if polarizacao_estado not in polarizacao_base:
        
        polarizacao_base.append(polarizacao_estado)
        estados_mesma_polarizacao.append([i])
    
    else:
        
        k = polarizacao_base.index(polarizacao_estado)
        estados_mesma_polarizacao[k].append(i)


## Tunelamento Coletivo

matriz_teve_tunelamento, matriz_numero_conectados, matriz_ordem, matriz_formato = Estados_Tunelados(base_H, polarizacao_base, estados_mesma_polarizacao, vizinhanca_rede)

Write_File(f'{pasta}/operador_ciclo/matriz_teve_tunelamento.txt', matriz_teve_tunelamento)
Write_File(f'{pasta}/operador_ciclo/matriz_numero_conectados.txt', matriz_numero_conectados)
Write_File(f'{pasta}/operador_ciclo/matriz_ordem.txt', matriz_ordem)
Write_File(f'{pasta}/operador_ciclo/matriz_formato.txt', matriz_formato)