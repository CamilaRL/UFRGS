import matplotlib.pyplot as plt

'''
    Plot energy (total, kinetic and potential), temperature, pressure versus timestep.
    Save the mean temperature and pressure in other file (used to plot the phase diagram)
'''

# Energy
def E_graph(file):

    T = []
    P = []
    K = []
    U = []
    E_tot = []
    t = []

    f = open(file, encoding='utf8')
    
    lines = f.readlines()[64:564] # ALTERAR CONFORME O ARQUIVO

    for line in lines:

        line = line.split(' ')
        while('' in line): line.remove('')

        t.append(float(line[0]))
        T.append(float(line[1]))
        U.append(float(line[2]))
        K.append(float(line[3]))
        E_tot.append(float(line[4]))
        P.append(float(line[5]))
        
    
    fig = plt.figure(figsize=(12,5))

    plt.subplot(131)
    plt.plot(t, E_tot, label='Total')
    plt.plot(t, U, label='Potencial')
    plt.plot(t, K, label='Cinética')
    plt.xlabel('Time')
    plt.ylabel('Energia')
    plt.title('Energias do Sistema')
    plt.legend()

    plt.subplot(132)    
    plt.plot(t, T)
    plt.xlabel('Time')
    plt.ylabel('T')
    plt.title('Temperatura do Sistema')

    plt.subplot(133)
    plt.plot(t, P)
    plt.xlabel('Time')
    plt.ylabel('P')
    plt.title('Pressão do Sistema')
    
    plt.tight_layout()
    plt.show()
    
    return t, T, P

def TxP_File(T, P, file):

    Tmean = sum(T[196:])/(len(t)-196)
    Pmean = sum(P[196:])/(len(t)-196)

    f = open(file, 'a')
    f.write(f'{Tmean} {Pmean}\n')
    f.close()


# MAIN

Tlist = ['0.20', '0.25', '0.30', '0.35', '0.40', '0.45', '0.50', '0.55']
#Tlist = ['0.35', '0.40', '0.45', '0.50', '0.55']

for T in Tlist:
    
    file_msd = f'C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\LAMMPS\\Two_Scale_Potential\\Results\\CaseB\\rho_001\\T{T}\\log.lammps'
    out1 = './PhasePoints100A.txt'

    t, T, P = E_graph(file_msd)
    #TxP_File(T, P, out1)







