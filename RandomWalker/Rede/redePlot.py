import matplotlib.pyplot as plt
import numpy as np

def walkerPlot(slist, bc):
    L = 20
    x = []
    y = []
    
    xi = []
    yi = []

    for i in range(len(slist)):
        
        if(bc[i] == 1):
            x.append(np.asarray(xi) + 0.5)
            y.append(np.asarray(yi) + 0.5)
            xi = []
            yi = []

        xi.append(slist[i]%L)
        yi.append(int(slist[i]/L))
    
    for i in range(len(x)):
        plt.plot(x[i], y[i], color='blue')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Posição do Caminhante - 1 amostra')
    plt.grid(True)
    plt.xticks(np.arange(0, 21, 1.0))
    plt.yticks(np.arange(0, 21, 1.0))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def desQuadPlot(step, dr2):

    plt.plot(step, dr2)
    plt.xlabel('Step')
    plt.ylabel(r'$R^2$')
    plt.title('Deslocamento Quadrático - 1 amostra')
    plt.grid(True)
    plt.show()

def msdPlot(step, dr2):
    
    p = np.zeros(1000)
    r2 = np.zeros(1000)
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
    x = np.arange(0, 1000, 0.1)
    #y = x**(3/2)
    y =x    

    #plot
    plt.plot(p, r2, label='Simulação')
    plt.plot(x, y, 'k-', label='y = x')
    plt.xlabel('Step')
    plt.ylabel('MSD')
    plt.title(f'Mean Square Displacement - {samp} amostras')
    plt.grid(True)
    plt.show()


N, w, x, y, dr2, bc = np.loadtxt('r.txt', unpack=True, comments='#')

walkerPlot(w[:1000], bc[:1000])
desQuadPlot(N[:1000], dr2[:1000])
msdPlot(N, dr2)
