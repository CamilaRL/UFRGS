import matplotlib.pyplot as plt
import numpy as np



def readFile(filename):

    with open(filename, 'r') as f:
        
        N = []
        P = []
        x = []

        lines = f.readlines()[2:]
        
        for line in lines:
            line = line.split(" ")

            N.append(int (line[0]))
            P.append(float (line[1]))
            x.append(float (line[2].strip('\n')))
    
    return N, P, x


N, I, x = readFile('I.txt')

'''
r = np.arange(0, 1.1, 0.01)
y = np.sin(1/r)**2
plt.plot(r, y, color='black')
plt.scatter(r1, r2, s=0.1)
plt.xlabel('theta')
plt.ylabel('1-y')
plt.show()'''


#fig = plt.figure(figsize=(15,5))

#plt.subplot(121)
plt.scatter(N[2000:], I[2000:], s=1)
plt.axhline(y = 0.673457, color = 'k', linestyle = '-', label='Analítico: 0.673457')
plt.ylabel('Integral')
plt.xlabel('N')
plt.title('Integração de sin^2(1/x) - Método do Círculo')
plt.legend()
plt.ticklabel_format(style='plain')
plt.show()
'''
y = np.power(np.array(N), -0.5)

plt.subplot(122)
plt.plot(N, I)
plt.plot(N, y)
plt.ylabel('log(|4n/- PI|)')
plt.xlabel('log(N)')
plt.yscale('log')
plt.xscale('log')

plt.suptitle('Estimativa do valor de pi - Método do Círculo')
plt.tight_layout()
plt.show()'''
