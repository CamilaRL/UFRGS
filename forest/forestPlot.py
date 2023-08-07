import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def readForest(filename):

    sitio, estado = np.loadtxt(filename, unpack=True, comments="#")
    
    forest = list(estado[i:(i+50)] for i in range(0, len(estado), 50))
    
    return sitio, forest

def readFire(filename):

    time = []
    fire = []

    with open(filename, 'r') as f:
    
        lines = f.readlines()[1:]
        
        for line in lines:
            
            line = line.split(" ")
            line = [float(l) for l in line[:-1]]
            
            time.append(line[0])
            fire.append([np.array(line[i:(i+50)], dtype='float') for i in range(1, len(line), 50)]) # devolver fire como matriz
        
    return time, fire
    
def forestPlot(forest, time):

    cmap = (mpl.colors.ListedColormap(['white', 'green', 'black']))

    image = plt.imshow(forest, cmap=cmap)
    plt.colorbar(ticks=[0, 1, 2])
    #plt.show()
    plt.imsave(f'./gif/{time}.png', image)

def SeparaAmostras(step, data):
    
    datai = []
    datat = []

    for i in range(len(step)):
    
        if((step[i] == 0.3) and (i>0)):
            datat.append(datai)
            datai = []
        
        datai.append(data[i])

        if(i == len(step)-1):
            datat.append(datai)
    
    return datat

def mediaAmostras(step, data):


    max = 0
    for s in step:
        if(len(s) > max):
            max = len(s)
    
    p = np.zeros(max) # passos
    t = np.zeros(max)
    k = 0
    samp = np.zeros(max) # contagem de quantas amostras foram feitas para cada passo de tempo

    for s in range(len(step)):
        for i in range(len(step[s])):
            
            p[i] = p[i] + step[s][i]
            t[i] = t[i] + data[s][i]
            
            samp[i] = samp[i] + 1
    
    for k in range(len(samp)):
        p[k] = p[k]/samp[k]
        t[k] = t[k]/samp[k]
        
    return p, t

def tempoQueimada():

    p, t = np.loadtxt('time50.txt', unpack=True, comments='#')
    
    p50 = SeparaAmostras(p, p)
    t50 = SeparaAmostras(p, t)
    
    p50, t50 = mediaAmostras(p50, t50)
    
    p, t = np.loadtxt('time100.txt', unpack=True, comments='#')
    
    p100 = SeparaAmostras(p, p)
    t100 = SeparaAmostras(p, t)
    
    p100, t100 = mediaAmostras(p100, t100)
   
    p, t = np.loadtxt('time150.txt', unpack=True, comments='#')
    
    p150 = SeparaAmostras(p, p)
    t150 = SeparaAmostras(p, t)
    
    p150, t150 = mediaAmostras(p150, t150)
 
    
    
    plt.scatter(p50, t50, label='L = 50')
    plt.scatter(p100, t100, label='L = 100')
    plt.scatter(p150, t150, label='L = 150')
    plt.axvline(x=0.5927, color='k', linestyle='--', label=r'$p_{c}$')
    plt.xlabel('p')
    plt.ylabel('T(p,L)')
    plt.legend()
    plt.show()


'''
sitio, estado = readForest('forest.txt')
forestPlot(estado, 0)

time, sistema = readFire('fire.txt')

for i in time:
    forestPlot(sistema[int(i)], i+1)'''
    
tempoQueimada()