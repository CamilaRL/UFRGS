import matplotlib.pyplot as plt
import numpy as np

def gridPlot():
    L = 50
    x = []
    y = []
    
    sitio, passou = np.loadtxt('syst.txt', unpack=True, comments='#')
    
    for i in range(len(passou)):
        if(passou[i] == 1):
        
            x.append((sitio[i] % L) + 0.5)
            y.append(int(sitio[i] / L) + 0.5)
    
    xi = (1470 % L) + 0.5
    yi = int(1470/L) + 0.5
    
    plt.scatter(x, y, color='blue')
    #plt.scatter(xi, yi, color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Posição do Caminhante na Rede')
    plt.grid(True, linewidth=0.5)
    plt.xticks(np.arange(0, 51, 1.0))
    plt.yticks(np.arange(0, 51, 1.0))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def walkerPlot(slist, bc):
    L = 50
    x = []
    y = []

    xi = []
    yi = []

    for i in range(len(slist)):
        
        if(bc[i] != 0):
            x.append(np.asarray(xi) + 0.5)
            y.append(np.asarray(yi) + 0.5)
            xi = []
            yi = []
        elif(i == len(slist)-1 and len(x) == 0):
            x.append(np.asarray(xi) + 0.5)
            y.append(np.asarray(yi) + 0.5)
        

        xi.append(slist[i]%L)
        yi.append(int(slist[i]/L))

    for i in range(len(x)):
        plt.plot(x[i], y[i], color='blue')
    
    plt.scatter(x[0][0], y[0][0], color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Posição do Caminhante - 1 amostra')
    plt.grid(True, linewidth=0.5)
    plt.xticks(np.arange(0, 51, 1.0))
    plt.yticks(np.arange(0, 51, 1.0))
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
    '''
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Posição do Caminhante - 1 amostra')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()'''

def desQuadPlot(step, dr2):
        #reta
    x = np.arange(0, 100, 0.1)
    y = x**(3/2)
    plt.plot(step, dr2)
    plt.plot(x, y, 'k-')
    plt.xlabel('Step')
    plt.ylabel(r'$R^2$')
    plt.title('Deslocamento Quadrático - 1 amostra')
    plt.grid(True)
    plt.show()

def msdPlot(step, dr2):

    max = 0
    for s in step:
        if(len(s) > max):
            max = len(s)
    
    p = np.zeros(max) # passos
    r2 = np.zeros(max)
    k = 0
    samp = np.zeros(max) # contagem de quantas amostras foram feitas para cada passo de tempo
    
    for s in range(len(step)):
        for i in range(len(step[s])):
            
            k = int(step[s][i])
            
            p[k] = p[k] + step[s][i]
            r2[k] = r2[k] + dr2[s][i]
            
            samp[k] = samp[k] + 1
    
    
    for k in range(len(samp)):
        p[k] = p[k]/samp[k]
        r2[k] = r2[k]/samp[k]
    
    #reta
    x = np.arange(0, 100, 0.1)
    y = x**(3/2)

    #plot
    plt.plot(p, r2, label='Simulação')
    plt.plot(x, y, 'k-', label='y = x')
    plt.xlabel('Step')
    plt.ylabel('MSD')
    plt.title(f'Mean Square Displacement')
    #plt.yscale('log')
    #plt.xscale('log')
    plt.grid(True)
    plt.show()

def SeparaAmostras(step, data):
    
    datai = []
    datat = []

    for i in range(len(step)):
        if(int(step[i]) == 0 or i == len(step)-1):
            datat.append(datai)
            datai = []
    
        datai.append(data[i])
    
    return datat


N, w, x, y, dr2, bc = np.loadtxt('ssamp.txt', unpack=True, comments='#')

step = SeparaAmostras(N,N)
w = SeparaAmostras(N,w)
x = SeparaAmostras(N,x)
y = SeparaAmostras(N,y)
dr2 = SeparaAmostras(N,dr2)
bc = SeparaAmostras(N,bc)


walkerPlot(w[1], bc[1])
desQuadPlot(step[1], dr2[1])
msdPlot(step, dr2)

