import matplotlib.pyplot as plt

'''
    Plot of phase diagram from files saved in graph_E.py. 
'''

def phase1(file):
    f = open(file, 'r')

    lines = f.readlines()
    T = []
    P = []

    for line in lines:
        line = line.split(' ')
        T.append(float(line[0]))
        P.append(float(line[1]))
    '''
    plt.plot(T, P)
    plt.xlabel('T')
    plt.ylabel('P')
    plt.title('Diagrama de fase')
    plt.show()'''

    return T, P

# each file has different density.
T1, P1 = phase1('PhasePoints001.txt')
T2, P2 = phase1('PhasePoints100A.txt')
T3, P3 = phase1('PhasePoints150.txt')

plt.plot(T1, P1, label='rho=0.01')
plt.plot(T2, P2, label='rho=0.100')
plt.plot(T3, P3, label='rho=0.150')
plt.ylim(top=1.0)
plt.xlabel('T')
plt.ylabel('P')
plt.title('Diagrama de fase')
plt.legend(loc=9)
plt.show()
