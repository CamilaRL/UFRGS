import numpy as np
import matplotlib.pyplot as plt

endereco_E = "C:\\Users\\camil\\Desktop\\UFRGS\\IC-Fluidos\\Programas\\Simulacoes\\energias.txt"
t, U, K, etot = np.loadtxt(endereco_E, skiprows = 1, unpack = True)

endereco_msd = "C:\\Users\\camil\\Desktop\\UFRGS\\IC-Fluidos\\Programas\\Simulacoes\\msd.txt"
teq, dr = np.loadtxt(endereco_msd, skiprows = 1, unpack = True)

endereco_G = "C:\\Users\\camil\\Desktop\\UFRGS\\IC-Fluidos\\Programas\\Simulacoes\\g_r.txt"
g, r = np.loadtxt(endereco_G, skiprows = 1, unpack = True)

# Gráfico da Energia pelo tempo
plt.scatter(t, U, color='red', s=0.1, label='Energia Potencial (U)')
plt.scatter(t, K, color='green', s=0.1, label='Energia Cinética (K)')
plt.scatter(t, etot, color='black', s=0.1, label='Energia Total (E)')
plt.xlabel('Tempo')
plt.ylabel('Energia')
plt.ylim(bottom=-5, top=5)
plt.legend(loc='right')
plt.title('Energia do Sistema', fontweight='bold')
plt.show()

plt.scatter(teq[100:], dr[100:], s=0.1)
plt.xlabel('Tempo')
plt.ylabel('MSD')
plt.title('Deslocamento Quadrático Médio', fontweight='bold')
plt.show()

plt.plot(r, g, 'k.')
plt.xlabel('r')
plt.ylabel('g(r)')
plt.title('Distribuição Radial', fontweight='bold')
plt.show()
'''
densidade_local = g*0.8442

plt.plot(r, densidade_local, 'k.')
plt.xlabel('r')
plt.ylabel('densidade local')
plt.ylim(top=3.5)
plt.show()'''