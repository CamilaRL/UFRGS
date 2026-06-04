import numpy as np
import matplotlib.pyplot as plt

# Energy
def E_graph(file):

    rho = []
    coef = []

    f = open(file)
    
    lines = f.readlines()

    for line in lines:

        line = line.split(' ')

        rho.append(float(line[0]))
        coef.append(float(line[1]))
        

    plt.plot(rho, coef)
    plt.xlabel('Densidade')
    plt.ylabel('Inclinacao')
    plt.show()    


# MAIN

file = './ajuste.txt'

E_graph(file)








