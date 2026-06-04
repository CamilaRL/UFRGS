import matplotlib.pyplot as plt

'''
    Plot of temperature versus density.
    Data extracted from media---.txt file created by graph averages.py
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
        P.append(float(line[1]))
        rho.append(float(line[2].strip('\n')))

    return T, P, rho

def graphic(rho, T):
    
    plt.scatter(T, rho)
    plt.xlabel('Temperatura')
    plt.ylabel('Densidade')
    plt.grid(True)
    plt.show()

x = '0.02' # alcohol concentration
eABlist = ['0.8', '1.1'] # potential parameter

for eAB in eABlist:
    file_path = f'./media{x}_{eAB}.txt'

    T, P, rho = read_file(file_path)

    plt.scatter(T, rho, label=f'eAB = {eAB}')

plt.xlabel('Temperatura')
plt.ylabel('Densidade')
plt.legend()
plt.title(f'x = {x}')
plt.grid(True)
plt.show()