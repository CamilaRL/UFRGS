import matplotlib.pyplot as plt
import numpy as np

def circulo(x):
    return np.sqrt(1-x**2)

def walkingplace(xc, yc, xs, ys):
    x_list = np.linspace(0, 1, 100)
    y = circulo(x_list)

    fig = plt.figure(figsize=(10,5))

    plt.subplot(121)
    plt.plot(x_list, y)
    plt.scatter(xc, yc, s=0.5)
    #plt.plot(xc, yc)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Com Rejeição')
    #plt.xlim(right=1, left=0)
    #plt.ylim(bottom=0, top=1)

    plt.subplot(122)
    plt.plot(x_list,y)
    plt.scatter(xs, ys, s=0.5)
    #plt.plot(xs, ys)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Sem Rejeição')

    plt.show()

def nN(Nc, Ns, ncc, nqc, ncs, nqs, title):

    nNc = ncc/nqc
    nNs = ncs/nqs

    plt.plot(Nc[:], nNc[:], label='Com Rejeição')
    plt.plot(Ns[:], nNs[:], label='Sem Rejeição')
    plt.axhline(y = np.pi/4, color = 'k', linestyle = '-', label=r'$\frac{\pi}{4}$')
    plt.ylabel('n/N')	
    plt.xlabel('N')
    plt.title(title)
    plt.legend()
    plt.show()

def histx(xc, xs):

    hist_c = list(int(x/0.01) for x in xc)
    hist_s = list(int(x/0.01) for x in xs)

    fig = plt.figure(figsize=(10,5))

    plt.subplot(121)
    plt.hist(hist_c, bins=100)
    plt.xlabel('x')
    plt.ylabel('Frequência')
    plt.title('Com Rejeição')
    plt.ylim(bottom=0, top=1200)

    plt.subplot(122)
    plt.hist(hist_s, bins=100)
    plt.xlabel('x')
    plt.ylabel('Frequência')
    plt.title('Sem Rejeição')
    plt.ylim(bottom=0, top=1200)

    plt.suptitle('1 Amostra com passo variável')
    plt.tight_layout()
    plt.show()
    
def histgauss(ncc, nqc, ncs, nqs):

    nNc = ncc/nqc
    nNs = ncs/nqs

    hist_c = list(int(x*4) for x in nNc)
    hist_s = list(int(x*4) for x in nNs)


    fig = plt.figure(figsize=(10,5))

    plt.subplot(121)
    plt.hist(hist_c, bins=100) #range=(3., 3.025)
    plt.xlabel('x')
    plt.ylabel('Frequência')
    plt.title('Com Rejeição')

    plt.subplot(122)
    plt.hist(hist_s, bins=100)
    plt.xlabel('x')
    plt.ylabel('Frequência')
    plt.title('Sem Rejeição')

    plt.suptitle('Média de amostras com passo variável')
    plt.tight_layout()
    plt.show()



######## MAIN #########

# ultimos dados de simulacao
Nc, nqc, ncc, xc, yc = np.loadtxt('./lastcr.txt', unpack=True, skiprows=2)
Ns, nqs, ncs, xs, ys = np.loadtxt('./lastsr.txt', unpack=True, skiprows=2)

# de uma amostra
aNc, anqc, ancc, axc, ayc = np.loadtxt('./sampcr.txt', unpack=True, comments='#', max_rows=100002)
aNs, anqs, ancs, axs, ays = np.loadtxt('./sampsr.txt', unpack=True, comments='#', max_rows=100002)


nN(aNc, aNs, ancc, anqc, ancs, anqs, '1 Amostra com passo variável')
histx(axc, axs)

nN(Nc, Ns, ncc, nqc, ncs, nqs, 'Média de amostras com passo variável')
histgauss(ncc, nqc, ncs, nqs)
histx(xc, xs)

