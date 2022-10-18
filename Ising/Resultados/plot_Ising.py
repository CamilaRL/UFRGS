import numpy as np
import matplotlib.pyplot as plt
import linecache as ln

def energia_plot(N, file):
    Emean = []
    for i in range(len(file)):
        t, E = np.loadtxt(file[i], unpack=True, skiprows=2)
        plt.plot(t, E, label=f'{file[i]} E')
        Emean.append(sum(E)/len(t))

    plt.ylabel('Energia')
    plt.xlabel('Tempo (MCS)')
    plt.legend()
    plt.title(f'Energia do Sistema Ising {N}x{N}')
    plt.show()

    return Emean

def magnetizacao_plot(N, file):
    Mmean = []
    for i in range(len(file)):
        t, M = np.loadtxt(file[i], unpack=True, skiprows=2)
        plt.plot(t, M, label=f'{file[i]} M')
        Mmean.append(sum(M)/len(t))
    
    plt.ylabel('Magnetização')
    plt.xlabel('Tempo (MCS)')
    plt.legend()
    plt.title(f'Magnetização do Sitema Ising {N}x{N}')
    plt.show()

    return Mmean

def spins_plot(N, file):
    t = []
    s = []
    col = np.arange(0, 10)
    lin = np.arange(0, 10)

    with open(file, 'r') as f:

        data = f.readlines()[2:]

        for k in range(len(data)):
            line = data[k].split('  ')
            t.append(int(line[0]))
            s.append(line[1].strip(' \n').split(' //'))

    print(s[0][0].split(', '))
    '''
    for j in lin:
        for i in col:
            print(f'{s[0][j][i]}', end='')
        print('new line')
        '''

def subplots_4T(N, t, E, T):
    fig = plt.figure(figsize=(10,5))

    plt.subplot(221)
    plt.plot(t[0], E[0])
    plt.ylabel('Energia')
    plt.xlabel('Tempo')  
    plt.title(f'Temperatura {T[0]}')

    plt.subplot(222)
    plt.plot(t[1], E[1])
    plt.ylabel('Energia')
    plt.xlabel('Tempo')    
    plt.title(f'Temperatura {T[1]}')

    plt.subplot(223)
    plt.plot(t[2], E[2])
    plt.ylabel('Energia')
    plt.xlabel('Tempo')      
    plt.title(f'Temperatura {T[2]}')

    plt.subplot(224)
    plt.plot(t[3], E[3])
    plt.ylabel('Energia')
    plt.xlabel('Tempo')  
    plt.title(f'Temperatura {T[3]}')

    plt.suptitle(f'Energia do Sistema Ising {N}x{N}')
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()

def propriedades_plot_temp(file):
    T = []
    P = []

    index = {"E":0, "M":1, "X":2, "C":3}
    ylabel = ['<E>', '<M>', 'X', 'C']
    title = ['Energia Média em função da Temperatura', 'Magnetização Média em função da Temperatura', 'Susceptibilidade em função da Temperatura', 'Calor Específico em função da Temperatura']

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
    y_min = 0
    y_max = 1
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

        if min(P)< y_min:
            y_min = min(P)
        if abs(max(P)) > y_max:
            y_max = max(P)

        T = []
        P = []

    
    plt.vlines(2.269, y_min, y_max, label='Tc = 2.269', colors='k')
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
'''
propriedades_plot_temp('energiaT.txt')
propriedades_plot_temp('magnetizacaoT.txt')
propriedades_plot_temp('susceptibilidadeT.txt')
propriedades_plot_temp('calorespecificoT.txt')

#energia_plot(10, fileE)
#magnetizacao_plot(10, fileM)

#spins_plot(10, 'spins1.txt')
'''
compare_plot_Nsys(filesE)
compare_plot_Nsys(filesM)
compare_plot_Nsys(filesX)
compare_plot_Nsys(filesC)