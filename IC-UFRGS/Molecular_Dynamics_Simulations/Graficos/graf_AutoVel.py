import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate

# Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_V = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\vac.txt"
teq_v, vac = np.loadtxt(endereco_V, skiprows = 1, unpack = True)

# Integração Numérica
Int_VAC = ((vac[0] + vac[-1])/2 + np.sum(vac[1:-1]))*teq_v[1]

difusao = integrate.simpson(vac, teq_v)

# Gráfico da Autocorrelação de Velocidades
plt.scatter(teq_v, vac, s=0.1, label=f'D: {Int_VAC}\n {difusao}')
plt.xlabel('Tempo')
plt.ylabel('VAC')
plt.title('Autocorrelação das velocidades', fontweight='bold')
plt.legend()
plt.show()