import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def readForest(filename):

    sitio, estado = np.loadtxt(filename, unpack=True, comments="#")
    
    return sitio, estado

def readFire(filename):

    time = []
    fire = []

    with open(filename, 'r') as f:
    
        lines = f.readlines()[1:]
        
        for line in lines:
            line = line.split(" ")
            print(len(lines))
            break
            t.append(line[0])
            #fire.append(line[1:])

def forestPlot(estado):

    forest = list(estado[i:(i+50)] for i in range(0, len(estado), 50))


    cmap = (mpl.colors.ListedColormap(['white', 'green', 'black']))

    plt.imshow(forest, cmap=cmap)
    plt.colorbar(ticks=[0, 1, 2])
    plt.show()


sitio, estado = readForest('forest.txt')
forestPlot(estado)

#readFire('fire.txt')