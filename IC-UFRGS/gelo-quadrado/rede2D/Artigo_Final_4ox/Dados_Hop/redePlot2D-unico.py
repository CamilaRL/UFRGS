import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plot_estado_listas(estado, N, hop):
    
    oxigenios_x = []
    oxigenios_y = []

    for oy in range(int(N/2), 0, -1):

        for ox in range(1, int(N/2)+1, 1):
            oxigenios_x.append(ox)
            oxigenios_y.append(oy)
    
    
    H_y = []
    H_x = []
    
    for i in range(0, len(estado), 2):
        
        k = int(i/2)
        
        if estado[i] == 1:
            H_x.append(oxigenios_x[k]-0.25)
            H_y.append(oxigenios_y[k])

        elif estado[i] == 2:
            H_x.append(oxigenios_x[k]+0.25)
            H_y.append(oxigenios_y[k])
            
        elif estado[i] == 3:
            H_x.append(oxigenios_x[k]+0.25)
            H_y.append(oxigenios_y[k])
            
            H_x.append(oxigenios_x[k]-0.25)
            H_y.append(oxigenios_y[k])


    for j in range(1, len(estado), 2):
        
        k = int(j/2)
        
        if estado[j] == 1:
            H_y.append(oxigenios_y[k]+0.25)
            H_x.append(oxigenios_x[k])

        elif estado[j] == 2:
            H_y.append(oxigenios_y[k]-0.25)
            H_x.append(oxigenios_x[k])
            
        elif estado[j] == 3:
            H_y.append(oxigenios_y[k]+0.25)
            H_x.append(oxigenios_x[k])
            
            H_y.append(oxigenios_y[k]-0.25)
            H_x.append(oxigenios_x[k])

    return H_x, H_y, oxigenios_x, oxigenios_y


def plot_estado(estado_n, estado_m, H_x_n, H_y_n, oxigenios_x_n, oxigenios_y_n, H_x_m, H_y_m, oxigenios_x_m, oxigenios_y_m):

    print(estado_n)
    print(estado_m)
    
    fig = plt.figure(figsize=(10,5))
    
    plt.subplot(121)
    plt.grid(True)
    plt.scatter(oxigenios_x_n, oxigenios_y_n, color='red')
    plt.scatter(H_x_n, H_y_n, color='blue', s=20)
    plt.title(f'Initial Configuration')
    plt.xlim((0.5,2.5))
    plt.ylim((0.5,2.5))
    
    plt.subplot(122)
    plt.grid(True)
    plt.scatter(oxigenios_x_m, oxigenios_y_m, color='red')
    plt.scatter(H_x_m, H_y_m, color='blue', s=20)
    plt.title(f'Final Configuration')
    plt.xlim((0.5,2.5))
    plt.ylim((0.5,2.5))
    
    plt.show()
    
    
def read_base(filename):
    base = []
    with open(filename, 'r') as f:
        
        lines = f.readlines()
        
        for line in lines:
            line = line.strip(' \n').split(' ')
            line = [float(l) for l in line]
            
            if len(line) > 1:
                base.append(line)
            
    return base

def read_autocoisas(filename):

    autovetor = []
    autovalor = []
    vetor = []
    i = 0

    with open(filename, "r") as f:
    
        lines = f.readlines()
        autocoisa = lines[0].strip("\n")
        
        for line in lines[1:]:
        
            line = line.strip("\n")
            
            if line == "Autovetores":
                autocoisa = line
            
            elif (autocoisa == "Autovetores") and (line != "Autovetores"):
                
                if(i==len(autovalor)):
                    autovetor.append(vetor)
                    i = 0
                    vetor = []
                    
                vetor.append(float(line))
                i = i + 1
            
            else:
                autovalor.append(float(line))
            
        autovetor.append(vetor)
        
    return autovalor, autovetor

########## MAIN ##########

N = 4
hop = 0.1
w = 1.2076933128681158

estados_base = read_base(f"./hopping-{hop}/{N}_baseO.txt")

val, vec = read_autocoisas(f"./hopping-{hop}/{N}_autocoisas.txt")

nList, mList = np.loadtxt(f'./hopping-{hop}/w_state/states-{w}.txt', unpack=True)


for i, n in enumerate(nList):
    
    print(int(n))
    print(int(mList[i]))
    
    vn = vec[int(n)]
    vm = vec[int(mList[i])]
    
    autovec_max_n = max(vn)
    autovec_max_m = max(vm)
    
    config_n = []
    config_m = []
    
    for j in range(len(vn)):
        
        if vn[j] == autovec_max_n:
            config_n.append(j)
        if vm[j] == autovec_max_m:
            config_m.append(j)
    
    plt.scatter(range(len(vn)), vn, s=10, label=f'n = {int(nList[i])}')
    plt.scatter(range(len(vm)), vm, s=10, label=f'm = {int(mList[i])}')
    plt.legend()
    plt.show()
    
    for c in range(len(config_n)):
        
        cn = config_n[c]
        cm = config_m[c]
        
        H_x_n, H_y_n, oxigenios_x_n, oxigenios_y_n = plot_estado_listas(estados_base[cn], N, hop)
        
        H_x_m, H_y_m, oxigenios_x_m, oxigenios_y_m = plot_estado_listas(estados_base[cm], N, hop)
    
        plot_estado(estados_base[cn], estados_base[cm], H_x_n, H_y_n, oxigenios_x_n, oxigenios_y_n, H_x_m, H_y_m, oxigenios_x_m, oxigenios_y_m)

