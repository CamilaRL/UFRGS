import matplotlib.pyplot as plt

'''
    Plot of TMD (temperature of maximum density) versus alcohol concentration.
    Data extracted from tmd---.txt file. The TMD values were obtained by observing the maximum on the curves temperature versus density.
    Another way for obtaining TMD values is using a polinomial fit.
'''

def read_file(file):
    
    T = []
    P = []
    rho = []

    f = open(file, 'r')
    lines = f.readlines()
    
    for line in lines:
        line = line.split(' ')
        while('' in line): line.remove('')

        T.append(float(line[0]))
        rho.append(float(line[1].strip('\n')))

    return T, rho


eAB = '1.1'

file_path = f'./tmd-{eAB}.txt'

x, rho = read_file(file_path)

plt.scatter(x, rho, label=f'eAB = {eAB}')

plt.xlabel('TMD')
plt.ylabel('Concentração (x)')
plt.legend()
plt.grid(True)
plt.show()