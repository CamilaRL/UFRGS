import matplotlib.pyplot as plt
import numpy as np

def walkerPlot(x, y):

    plt.plot(x, y)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Posição do Caminhante - 1 amostra')
    plt.grid(True)
    plt.show()

def desQuadPlot(step, dr2):

    plt.plot(step, dr2)
    plt.xlabel('Step')
    plt.ylabel(r'$R^2$')
    plt.title('Deslocamento Quadrático - 1 amostra')
    plt.grid(True)
    plt.show()

def msdPlot(step, dr2):
    
    p = np.zeros(10000)
    r2 = np.zeros(10000)
    k = 0
    samp = 0
    
    for i in range(len(step)):

        if(int(step[i]) == 0):
            samp = samp + 1
        
        k = int(step[i])

        p[k] = p[k] + step[i]

        r2[k] = r2[k] + dr2[i]
    
    p = p/samp
    r2 = r2/samp
    
    #reta
    x = np.arange(0, 10000, 0.1)
    y = x
    
    #plot
    plt.plot(p, r2, label='Simulação')
    plt.plot(x, y, 'k-', label='y = x')
    plt.xlabel('Step')
    plt.ylabel('MSD')
    plt.title(f'Mean Square Displacement - {samp} amostras')
    plt.grid(True)
    plt.show()


N, x, y, dr2 = np.loadtxt('w.txt', unpack=True, comments='#')

walkerPlot(x[:10000], y[:10000])
desQuadPlot(N[:10000], dr2[:10000])
msdPlot(N, dr2)


'''
Algoritmo Roches-Coperman = medida de cluster
'''
