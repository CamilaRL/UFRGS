import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm


hop = 1.0

'''
wAnomalia = np.loadtxt(f'./superposicao_anomalia_{hop}.txt', unpack=True, ndmin=1, usecols=(0))
superAnomalia = np.loadtxt(f'./superposicao_anomalia_{hop}.txt', unpack=True, ndmin=1, usecols=(1))
totAnomalia = np.loadtxt(f'./superposicao_anomalia_{hop}.txt', unpack=True, ndmin=1, usecols=(2))

porcentagem_Anomalia = []
for i, w in enumerate(wAnomalia):
    
    porcentagem_Anomalia.append(superAnomalia[i]/totAnomalia[i])
    

wAnomalia, porcentagem_Anomalia = (list(t) for t in zip(*sorted(zip(wAnomalia, porcentagem_Anomalia))))
'''

wOutros, superOutros, totOutros = np.loadtxt(f'./superposicao_outros_{hop}.txt', unpack=True, usecols=(0,1,2))

porcentagem_Outros = []
w_igual1 = []
w_igual0 = []
w_diferente = []

for i, w in enumerate(wOutros):
    
    p = superOutros[i]/totOutros[i]
    porcentagem_Outros.append(p)
    
    if p == 1:
        w_igual1.append(w)
    elif p == 0:
        w_igual0.append(w)
    else:
        w_diferente.append(w)

wOutros, porcentagem_Outros = (list(t) for t in zip(*sorted(zip(wOutros, porcentagem_Outros))))


plt.scatter(wOutros, porcentagem_Outros, color='black', s=10, label='Normal')
#plt.scatter(wAnomalia, porcentagem_Anomalia, color='blue', s=10, label='Anomaly')

plt.ylabel('Superposition Percentage (%)')
plt.xlabel('Frequency')
plt.legend()
plt.show()


color = iter(cm.rainbow(np.linspace(0, 1, len(w_igual0))))

for w in w_igual0:

    T, chi = np.loadtxt(f'../Dados_Hop/hopping-{hop}/chiTempOutput/chiTemp-{w}.txt', unpack=True)
    c = next(color)
    plt.plot(T, chi, color=c, label=f'{w:.5f}')
    
plt.title('0% Superposition')
plt.ylabel('Imaginary Susceptibility')
plt.xlabel('Temperature')
plt.show()


color = iter(cm.rainbow(np.linspace(0, 1, len(w_igual1))))

for w in w_igual1:
    
    T, chi = np.loadtxt(f'../Dados_Hop/hopping-{hop}/chiTempOutput/chiTemp-{w}.txt', unpack=True)
    c = next(color)
    plt.plot(T, chi, color=c, label=f'{w:.5f}')
    
plt.title('100% Superposition')
plt.ylabel('Imaginary Susceptibility')
plt.xlabel('Temperature')
plt.show()

color = iter(cm.rainbow(np.linspace(0, 1, len(w_diferente))))

for w in w_diferente:
    
    T, chi = np.loadtxt(f'../Dados_Hop/hopping-{hop}/chiTempOutput/chiTemp-{w}.txt', unpack=True)
    c = next(color)
    plt.plot(T, chi, color=c, label=f'{w:.5f}')
    
plt.title('Some Superposition')
plt.ylabel('Imaginary Susceptibility')
plt.xlabel('Temperature')
plt.show()