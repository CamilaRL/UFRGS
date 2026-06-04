from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

## Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_E = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\energias.txt"
t, U, K, etot = np.loadtxt(endereco_E, skiprows = 1, unpack = True)

endereco_msd = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\msd.txt"
teq, dr = np.loadtxt(endereco_msd, skiprows = 1, unpack = True)

endereco_G = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\g_r.txt"
g, r = np.loadtxt(endereco_G, skiprows = 1, unpack = True)


## Graficos
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15,4))

# Energias
ax1.scatter(t, U, color='red', s=0.1, label='Energia Potencial (U)')
ax1.scatter(t, K, color='green', s=0.1, label='Energia Cinética (K)')
ax1.scatter(t, etot, color='black', s=0.1, label='Energia Total (E)')
ax1.set_xlabel('Tempo')
ax1.set_ylabel('Energia')
ax1.legend(loc='right')
ax1.set_title('Energia do Sistema', fontweight='bold')

# Distribuição Radial
ax2.plot(r, g, 'k.')
ax2.set_xlabel('r')
ax2.set_ylabel('g(r)')
ax2.set_title('Distribuição Radial', fontweight='bold')

# MSD
ax3.scatter(teq, dr, s=0.1)
ax3.set_xlabel('Tempo')
ax3.set_ylabel('MSD')
ax3.set_title('Deslocamento Quadrático Médio', fontweight='bold')

fig.tight_layout()
plt.show()