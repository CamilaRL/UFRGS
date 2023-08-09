import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation


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
    
def forestPlot(forest):

    cmap = (mpl.colors.ListedColormap(['white', 'green', 'black']))

    image = plt.imshow(forest, cmap=cmap)
    plt.colorbar(ticks=[0, 1, 2])
    plt.show()

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


    #L = [50, 80, 100, 120, 180]
    L = [50]
    for l in L:
        pout, tout = np.loadtxt(f'./Output/time.txt', unpack=True, comments='#')
    
        p = SeparaAmostras(pout, pout)
        t = SeparaAmostras(pout, tout)
    
        p, t = mediaAmostras(p, t)
        
        plt.scatter(p, t, label=f'L = {l}')
        
    plt.axvline(x=0.5927, color='k', linestyle='--', label=r'$p_{c}$')
    plt.xlabel('p')
    plt.ylabel('T(p,L)')
    plt.legend()
    plt.show()


# animation

def run(frame, im, t):
    '''
    Roda a animação com os dados fornecidos por 'data'
    '''
    cmap = (mpl.colors.ListedColormap(['white', 'green', 'black']))
    im.set_array(frame)
    t += 1
    plt.title('Forest Fire\n'+'p = 0.5'+f't = {t}')

def gifForest(estados):

    fig, ax = plt.subplots()
    plt.xticks([]), plt.yticks([])

    cmap = (mpl.colors.ListedColormap(['white', 'green', 'black']))
    im = plt.imshow(estados[0], origin='lower', cmap=cmap)
    t = 0
    
    ani = animation.FuncAnimation(fig, run, frames=estados, fargs=(im, t), interval=100, blit=False) #save_count=1500
    
    # Escolha o formato da animação desejado, gif ou mp4:
    #writergif = animation.PillowWriter(fps=30)
    #ani.save('./florestFire.gif', writer=writergif)

    FFwriter = animation.FFMpegWriter(fps=40)
    ani.save('./florestFire.mp4', writer=FFwriter, dpi=400)

    plt.close()


#sitio, estado = readForest('./Output/forest.txt')
#forestPlot(estado, 0)

#time, sistema = readFire('./Output/fire.txt')

#forestPlot(sistema[-1])

#gifForest(sistema)
    
tempoQueimada()

