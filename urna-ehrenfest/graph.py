import matplotlib.pyplot as plt
import numpy as np

def readFile(filename):

    with open(filename, 'r') as f:
        
        t = []
        A = []

        lines = f.readlines()[1:]
        
        for line in lines:
            line = line.split(" ")

            t.append(int (line[0]))
            A.append(float (line[1].strip('\n')))
    
    return t, A

def binomial(N, nlist):
    dist = []
    for n in nlist:
        dist.append((1/2**N)*(np.math.factorial(N))/(np.math.factorial(n)*np.math.factorial(N-n)))
    
    return dist


# MAIN

n = np.arange(0, 100)

n, hist = readFile("hist.txt")

dist = binomial(100, n)


plt.plot(n[20:80], hist[20:80], 'b.', label="Simulação")
plt.plot(n[20:80], dist[20:80], 'k-', label='Distribuição Binomial')
plt.legend()
plt.title("Distribuição de Bolas na Caixa")
plt.xlabel("n")
plt.ylabel("Nn/N")
plt.show()
