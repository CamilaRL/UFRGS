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
    
    xi = (2350% L) + 0.5
    yi = int(2350/L) + 0.5
    xf = (1425 % L) + 0.5
    yf = int(1425/L) + 0.5

    
    plt.scatter(x, y, color='blue')
    plt.scatter(xi, yi, color='green')
    plt.scatter(xf, yf, color='red')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Posição do Caminhante na Rede')
    plt.grid(True, linewidth=0.5)
    plt.xticks(np.arange(0, 51, 1.0), color='w')
    plt.yticks(np.arange(0, 51, 1.0), color='w')
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def walkerPlot(slist, bc):
    L = 50
    x = []
    y = []

    xi = []
    yi = []

    for i in range(len(slist)):
    
        if(bc[i] != 0 and i>0):

            x.append(np.asarray(xi) + 0.5)
            y.append(np.asarray(yi) + 0.5)
            xi = []
            yi = []

        xi.append(slist[i]%L)
        yi.append(int(slist[i]/L))

        if(i == len(slist)-1):
            x.append(np.asarray(xi) + 0.5)
            y.append(np.asarray(yi) + 0.5)

    for i in range(len(x)):
        plt.plot(x[i], y[i], color='blue')

    plt.scatter(x[0][0], y[0][0], color='green', label='inicial')
    plt.scatter(x[-1][-1], y[-1][-1], color='red', label='final')
    '''plt.xlabel('x')
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
    plt.ylim(bottom=0, top=L)
    plt.xlim(left=0, right=L)
    
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def desQuadPlot(step, dr2):

    plt.plot(step, dr2)
    plt.plot(x, y, 'k-')
    plt.xlabel('Step')
    plt.ylabel(r'$R^2$')
    plt.title('Deslocamento Quadrático - 1 amostra')
    plt.grid(True)
    plt.show()

def msdPlot(step, dr2):

    print('Iniciando MSD')

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
    x = np.arange(10, max-80, 0.1)
    y = x**(3/2)
    print('Grafico da MSD')
    #plot
    plt.plot(p, r2, label='Simulação')
    plt.plot(x, y, 'k-', label='y = x')
    plt.xlabel('Step')
    plt.ylabel('MSD')
    plt.title(f'Mean Square Displacement')
    plt.yscale('log')
    plt.xscale('log')
    plt.xlim(left=1)
    plt.ylim(bottom=1)
    plt.grid(True)
    plt.show()

def SeparaAmostras(step, data):
    
    datai = []
    datat = []

    for i in range(len(step)):
    
        if((int(step[i]) == 0) and (i>0)):
            datat.append(datai)
            datai = []
        
        datai.append(data[i])

        if(i == len(step)-1):
            datat.append(datai)
    
    return datat

N = []
w = []
x = []
y = []
dr2 = []
bc = []

for i in range(3):

    print(f'File {i}')
    N1, w1, dr21, bc1 = np.loadtxt(f'ssamp{i}.txt', unpack=True, comments='#', usecols=(0,1,4,5))
    
    for j in range(len(N1)):
        N.append(N1[j])
        w.append(w1[j])
        dr2.append(dr21[j])
        bc.append(bc1[j])

step = SeparaAmostras(N,N)
w = SeparaAmostras(N,w)
dr2 = SeparaAmostras(N,dr2)
bc = SeparaAmostras(N,bc)

walkerPlot(w[5112], bc[5112])
desQuadPlot(step[5112], dr2[5112])
msdPlot(step, dr2)
#gridPlot()
