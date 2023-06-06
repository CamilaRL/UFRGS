import matplotlib.pyplot as plt
import numpy as np



def readFile(filename):

    with open(filename, 'r') as f:
        
        N = []
        P = []
        r1 = []
        r2 = []

        lines = f.readlines()[1:]
        
        for line in lines:
            line = line.split(" ")

            N.append(int (line[0]))
            P.append(float (line[1]))
            r1.append(float (line[2]))
            r2.append(float (line[3].strip('\n')))
    
    return N, P, r1, r2


N, P, r1, r2 = readFile('P.txt')

theta = np.arange(0, np.pi, 100)
y = np.sin(theta)

plt.plot(theta, y, color='black')
plt.scatter(r1, r2, s=0.1)
plt.xlabel('theta')
plt.ylabel('1-y')
plt.show()


plt.scatter(N, P, s=1)
plt.ylabel('2N/n')
plt.xlabel('N')
plt.show()

P1 = np.abs(np.array(P) - np.pi)
plt.scatter(N[80:], P1[80:], s=1)
plt.ylabel('|2N/n - PI|')
plt.xlabel('N')
plt.show()

y = np.power(np.array(N), -0.5)
plt.plot(N, P1)
plt.plot(N, y)
plt.ylabel('log(|2N/n - PI|)')
plt.xlabel('log(N)')
plt.yscale('log')
plt.xscale('log')
plt.show()

