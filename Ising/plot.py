import numpy as np
import matplotlib.pyplot as plt
import linecache as ln



def propriedades_plot_temp(file):
    T = []
    P = []

    index = {"E":0, "M":1, "X":2, "C":3}
    ylabel = ['<E>', '<M>', 'X', 'C']
    #title = ['Energia Média em função da Temperatura', 'Magnetização Média em função da Temperatura', 'Susceptibilidade em função da Temperatura', 'Calor Específico em função da Temperatura']

    line = ln.getline(file, 2).split(" ")
    prop = line[1].strip("\n")
    
    with open(file, 'r') as f:

        data = f.readlines()[2:]
        for i in range(len(data)):
            item = data[i].split(" ")
            T.append(float(item[0]))
            P.append(float(item[1]))
        
    plt.plot(T, P)
    plt.ylabel(ylabel[index[prop]])
    plt.xlabel('Temperatura')
    plt.title(title[index[prop]])
    plt.show()

def compare_plot_Nsys(file):
    T = []
    P = []

    index = {"E":0, "M":1, "X":2, "C":3}
    ylabel = ['<E>', '<M>', 'X', 'C']
    title = ['Energia Média em função da Temperatura', 'Magnetização Média em função da Temperatura', 'Susceptibilidade em função da Temperatura', 'Calor Específico em função da Temperatura']

    line = ln.getline(file[0], 2).split(" ")
    prop = line[1].strip("\n")

    for i in range(len(file)):
        line = ln.getline(file[i], 1).split(" ")
        N = line[2].strip("\n")
    
        with open(file[i], 'r') as f:

            data = f.readlines()[2:]
            for i in range(len(data)):
                item = data[i].split(" ")
                T.append(float(item[0]))
                P.append(float(item[1]))
        
        plt.scatter(T, P, s = 1, label=f'{N}x{N}')
        T = []
        P = []

    plt.ylabel(ylabel[index[prop]])
    plt.xlabel('Temperatura')
    plt.legend()
    plt.title(title[index[prop]])
    plt.show()


filesE = ['energiaT_10.txt', 'energiaT_20.txt', 'energiaT_30.txt']
filesM = ['magnetizacaoT_10.txt', 'magnetizacaoT_20.txt', 'magnetizacaoT_30.txt']
filesX = ['susceptibilidadeT_10.txt', 'susceptibilidadeT_20.txt', 'susceptibilidadeT_30.txt']
filesC = ['calorespecificoT_10.txt', 'calorespecificoT_20.txt', 'calorespecificoT_30.txt']
fileE = ['energia.txt']
fileM = ['magnetizacao.txt']

propriedades_plot_temp('energiaT.txt')
propriedades_plot_temp('magnetizacaoT.txt')
propriedades_plot_temp('susceptibilidadeT.txt')
propriedades_plot_temp('calorespecificoT.txt')

#energia_plot(10, fileE)
#magnetizacao_plot(10, fileM)

#spins_plot(10, 'spins1.txt')

#compare_plot_Nsys(filesE)
#compare_plot_Nsys(filesM)
#compare_plot_Nsys(filesX)
#compare_plot_Nsys(filesC)
