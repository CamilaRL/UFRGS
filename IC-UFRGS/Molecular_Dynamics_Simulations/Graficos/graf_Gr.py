import numpy as np
import matplotlib.pyplot as plt

# Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_G = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\g_r.txt"
g, r = np.loadtxt(endereco_G, skiprows = 1, unpack = True)

# Grafico da distribuição radial
plt.plot(r, g, 'k.')
plt.xlabel('r')
plt.ylabel('g(r)')
plt.title('Distribuição Radial', fontweight='bold')
plt.show()

# Grafico da densidade local
densidade_local = g*0.8442

plt.plot(r, densidade_local, 'k.')
plt.xlabel('r')
plt.ylabel('densidade local')
plt.ylim(top=3.5)
plt.show()
