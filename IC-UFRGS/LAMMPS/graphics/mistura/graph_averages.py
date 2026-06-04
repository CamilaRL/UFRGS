import matplotlib.pyplot as plt

def extract_data(file):
    T = []
    P = []
    rho = []
    H = []
    step = []

    f = open(file, encoding='utf8')
    
    lines = f.readlines()[2:] # ALTERAR CONFORME O ARQUIVO

    for line in lines:

        line = line.split(' ')
        while('' in line): line.remove('')

        step.append(float(line[0]))
        T.append(float(line[1]))
        P.append(float(line[2]))
        rho.append(float(line[3]))
        H.append(float(line[4]))

    return step, T, P, rho, H

def graphic(step, T, P, E):

    fig = plt.figure(figsize=(12,5))

    plt.subplot(131)
    plt.plot(step, T)
    plt.xlabel('Time Step')
    plt.ylabel('Temperatura')
    plt.title('Temperatura do Sistema')

    plt.subplot(132)
    plt.plot(step, P)
    plt.xlabel('Time Step')
    plt.ylabel('Pressão')
    plt.title('Pressão do Sistema')

    plt.subplot(133)
    plt.plot(step, E)
    plt.xlabel('Time Step')
    plt.ylabel('Energia Total')
    plt.title('Energia Total do Sistema')
    
    plt.tight_layout()
    plt.show()

def media(t, T, P, rho, file):

    Tmean = sum(T[196:])/(len(t)-196)
    Pmean = sum(P[196:])/(len(t)-196)
    rhomean = sum(rho[196:])/(len(t)-196)

    f = open(file, 'a')
    f.write(f'{Tmean} {Pmean} {rhomean}\n')
    f.close()

Tlist = ['0.30', '0.35', '0.40', '0.45', '0.50', '0.55', '0.60']
xlist = ['0.03']
eAB = '1.1'

for x in xlist:
    for Titem in Tlist:
        
        file_path = f'../results/eAB-{eAB}/c_{x}/P_0.13/T_{Titem}/averages.dat'

        t, T, P, rho, H = extract_data(file_path)
        
        E = []
        for i in range(len(rho)):
            V = 1000/rho[i]
            e = H[i] - V*P[i]
            E.append(e)

        #graphic(t, T, P, E)
        media(t, T, P, rho, f'media{x}_{eAB}.txt')
