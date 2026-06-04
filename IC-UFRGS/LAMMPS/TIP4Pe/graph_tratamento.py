import matplotlib.pyplot as plt

'''
    Plot energy (total, kinetic and potential), temperature, pressure versus timestep.
    Save the mean temperature and pressure in other file (used to plot the phase diagram)
'''

# Energy
def extractData(file, linit, lfinal):

    T = []
    P = []
    K = []
    U = []
    E_tot = []
    t = []

    f = open(file, encoding='utf8')
    
    lines = f.readlines()[linit:lfinal] # ALTERAR CONFORME O ARQUIVO // 1420
    line = []
    i = 0

    while(i < len(lines)):

        line = lines[i].split(' ')
        while('' in line): line.remove('')

        if(line[0] != 'SHAKE'):
            t.append(float(line[0]))
            T.append(float(line[1]))
            #U.append(float(line[2]))
            #K.append(float(line[3]))
            E_tot.append(float(line[3]))
            P.append(float(line[2]))
            i = i + 1

        elif(line[0] == 'SHAKE'):
            i = i + 3
    lim = 100
    
    return t, T, P, E_tot, lim
    
def E_graph(t, E_tot, lim):

    plt.plot(t[lim:], E_tot[lim:], label='Total')
    #plt.plot(t[lim:], U[lim:], label='Potencial')
    #plt.plot(t[lim:], K[lim:], label='Cinética')
    plt.xlabel('Time')
    plt.ylabel('Energia (kcal/mol)')
    plt.title('Energias do Sistema')
    plt.legend()
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.title('rho = 1.05 (g/cm^3)')
    plt.show()
    
def T_graph(t, T, lim):
    
    plt.plot(t[lim:], T[lim:])
    plt.xlabel('Time')
    plt.ylabel('T (Kelvin)')
    plt.title('Temperatura do Sistema')
    plt.axhline(y=1000, color='black', label='1000 K')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.legend(loc=3)
    plt.title('rho = 1.05 (g/cm^3)')
    plt.show()
    
def P_graph(t, P, lim):

    plt.plot(t[lim:], P[lim:])
    plt.axhline(y=1480.3849, color='black', label='Objetivo: 1480.385 atm = 150 MPa')
    plt.axhline(y=-684.6485960509206, color='purple', label='Simulacao: -684.648 atm = -0.069 MPa')
    plt.xlabel('Time')
    plt.ylabel('P (atm)')
    plt.title('Pressão do Sistema')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.legend(loc=3)
    plt.title('rho = 1.05 (g/cm^3)')
    plt.show()
    
def ALL_graph(t, T, P, E_tot, lim):
    fig = plt.figure(figsize=(12,5))
	
    plt.subplot(131)
    plt.plot(t[lim:], E_tot[lim:], label='Total')
    #plt.plot(t[lim:], U[lim:], label='Potencial')
    #plt.plot(t[lim:], K[lim:], label='Cinética')
    plt.xlabel('Time')
    plt.ylabel('Energia (kcal/mol)')
    plt.title('Energias do Sistema')
    #plt.legend()
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

    plt.subplot(132)    
    plt.plot(t[lim:], T[lim:])
    plt.xlabel('Time')
    plt.ylabel('T (Kelvin)')
    plt.title('Temperatura do Sistema')
    #plt.axhline(y=800, color='black', label='800 K')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #plt.legend()

    plt.subplot(133)
    plt.plot(t[lim:], P[lim:])
    #plt.axhline(y=1480.385, color='black', label='Objetivo: 1480.385 atm = 150 MPa')
    plt.xlabel('Time')
    plt.ylabel('P (atm)')
    plt.title('Pressão do Sistema')
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    #plt.legend(loc=3)

    plt.suptitle('rho = 1.05 (g/cm^3)')
    plt.tight_layout()
    plt.show()

def MeanFile(T, P, file, cut):

    Tmean = sum(T[cut:])/(len(t)-cut)
    Pmean = sum(P[cut:])/(len(t)-cut)

    f = open(file, 'a')
    f.write(f'{Tmean} {Pmean} {cut}\n')
    f.close()


# MAIN

number_files = int(input('Número de arquivos analisados: '))

for i in range(number_files):

    file = input('Arquivo log.lammps: ')
    linit = int(input('Linha incial de leitura: '))
    lfinal = int(input('Linha final de leitura: '))
    if(i == 0):
        t, T, P, E, lim = extractData(file, linit, lfinal)

    if(i > 0):
        taux, Taux, Paux, Eaux, lim_aux = extractData(file, linit, lfinal)
        
        t = t + taux
        T = T + Taux
        P = P + Paux
        E = E + Eaux
        lim = lim + lim_aux

ALL_graph(t, T, P, E, lim)


val = int(input('Fazer médias? (0 - não ou 1 - sim): '))
continua = 1
if(val == 1):
    while(continua == 1):
        cut = int(input('Corte para início da média: '))
        ALL_graph(t[cut:], T[cut:], P[cut:], E[cut:], lim)
        continua = int(input('Tentar novamente? (0 - não ou 1 - sim): '))

    file = input('Endereço do arquivo de saida: ')
    file = file + 'meanFile.txt'
    MeanFile(T, P, file, cut)
