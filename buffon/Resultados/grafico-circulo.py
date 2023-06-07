import matplotlib.pyplot as plt
import numpy as np



def readFile(filename):

    with open(filename, 'r') as f:
        
        N = []
        P = []
        r1 = []
        r2 = []

        lines = f.readlines()[2:]
        
        for line in lines:
            line = line.split(" ")

            N.append(int (line[0]))
            P.append(float (line[1]))
            r1.append(float (line[2]))
            r2.append(float (line[3].strip('\n')))
    
    return N, P, r1, r2


#N, P, r1, r2 = readFile('Pi-cir-huge.txt')
N, P, r1, r2 = readFile('Pi-cir.txt')

'''
r = np.arange(0, 1.1, 0.01)
y = np.sqrt(1-r**2)
plt.plot(r, y, color='black')
plt.scatter(r1, r2, s=0.1)
plt.xlabel('theta')
plt.ylabel('1-y')
plt.show()'''


fig = plt.figure(figsize=(15,5))

plt.subplot(131)
plt.scatter(N[1000:], P[1000:], s=1)
plt.axhline(y = np.pi, color = 'k', linestyle = '-')
plt.ylabel('4n/N')
plt.xlabel('N')

P1 = np.abs(np.array(P) - np.pi)

plt.subplot(132)
plt.scatter(N[1000:], P1[1000:], s=1)
plt.axhline(y = 0, color = 'k', linestyle = '-')
plt.ylabel('|4n/N - PI|')
plt.xlabel('N')

y = np.power(np.array(N), -0.5)

plt.subplot(133)
plt.plot(N, P1)
plt.plot(N, y, label='x^(-1/2)')
plt.ylabel('log(|4n/N - PI|)')
plt.xlabel('log(N)')
plt.yscale('log')
plt.xscale('log')
plt.legend()

plt.suptitle('Estimativa do valor de pi - Método do Círculo')
plt.tight_layout()
plt.show()
