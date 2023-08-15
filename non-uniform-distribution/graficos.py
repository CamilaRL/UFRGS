import numpy as np
import matplotlib.pyplot as plt

def plot_ex3():
    gamma = -0.8

    step1, I1 = np.loadtxt("./saida-08", unpack=True, comments='#')
    step2, I2 = np.loadtxt("./saida08", unpack=True, comments='#')

    Ianalitico = 1/(1+gamma)

    fig = plt.figure(figsize=(10,5))

    plt.subplot(121)
    plt.plot(step1[50:], I1[50:])
    plt.axhline(y=Ianalitico, color = 'k', linestyle = '-', label='Analítico')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel(f'I({gamma:.2f})')
    plt.title(r'$\gamma = -0.8$')
    
    gamma = 0.8
    Ianalitico = 1/(1+gamma)

    plt.subplot(122)
    plt.plot(step2[50:], I2[50:])
    plt.axhline(y=Ianalitico, color = 'k', linestyle = '-', label='Analítico')
    plt.xlabel('x')
    plt.ylabel(f'I({gamma:.2f})')
    plt.title(r'$\gamma = 0.8$')

    plt.legend()
    plt.show()

def hist(data, bins):

    index = np.linspace(min(data), max(data)+1, bins)
    hist = np.zeros(bins)
    binsize = (max(data)+1 - min(data))/bins

    for d in data:
        '''k = 0
        bin_max_value = index[k]

        while(d > bin_max_value):
            k = k + 1
            bin_max_value = index[k]
            
        hist[k] = hist[k] + 1
        '''

        k = (int) (d/binsize)
        hist[k] = hist[k] + 1
    
    # normalizacao
    norm = sum(hist)/10

    print(norm)
    hist = hist/norm

    # plot exponencial
    xlist = np.arange(0, 12, 0.1)
    y = list(np.exp(-x) for x in xlist)
    
    plt.plot(xlist, y, label='Analítico')
    plt.scatter(index, hist)
    #plt.yscale('log')
    plt.show()
    
def plot_hist_dist():
    xlist = np.arange(0, 3, 0.001)
    #y = list(np.exp(-x) for x in xlist) #ex5
    y = list((1-0.4)*x**(-0.4) for x in xlist) #ex6

    x = np.loadtxt("./saida", unpack=True, comments='#')

    
    plt.hist(x, bins=100, density=True, color='lightblue')
    plt.plot(xlist, y, label='Analitico', color='black')
    plt.ylabel('p(x)')
    plt.xlabel('x')
    plt.xlim(left=0.01, right=1)
    plt.legend()
    plt.show()

    plt.hist(x, bins=100, density=True, color='lightblue')
    plt.plot(xlist, y, label='Analitico', color='black')
    plt.ylabel('p(x)')
    plt.xlabel('x')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlim(left=0.01, right=1)
    plt.legend()
    plt.show()

def plot_ex11():
    gamma = -0.8
    Ianalitico = 1/(1+gamma)

    step1, I1 = np.loadtxt("./saida11", unpack=True, comments='#')
    step2, I2 = np.loadtxt("./saida-08", unpack=True, comments='#')

    plt.plot(step1[50:], I1[50:], label='Distribuição não-uniforme')
    plt.plot(step2[50:], I2[50:], label='Distribuição uniforme')
    plt.axhline(y=Ianalitico, color = 'k', linestyle = '-', label='Analítico')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel(f'I({gamma:.2f})')
    plt.title(r'$\gamma = -0.8$')
    plt.show()

def plot_px():
	r, x = np.loadtxt("./dist", unpack=True, comments='#')
	
	plt.hist(x, bins=100)
	plt.xlabel('x')
	plt.ylabel('Frequência')
	plt.title('Distribuição P(x)')
	plt.show()

plot_px()
#plot_ex3()
plot_ex11()

#plot_hist_dist()
#x = np.loadtxt("./saida", unpack=True, comments='#')
#hist(x,100)
