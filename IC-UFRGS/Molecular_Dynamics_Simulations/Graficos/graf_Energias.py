import numpy as np
import matplotlib.pyplot as plt

# Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_E = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\energias.txt"
t, U, K, etot = np.loadtxt(endereco_E, skiprows = 1, unpack = True)

# Gráfico da Energia pelo tempo
plt.scatter(t, U, color='red', s=0.1, label='Energia Potencial (U)')
plt.scatter(t, K, color='green', s=0.1, label='Energia Cinética (K)')
plt.scatter(t, etot, color='black', s=0.1, label='Energia Total (E)')
plt.xlabel('Tempo')
plt.ylabel('Energia')
plt.legend(loc='right')
plt.title('Energia do Sistema', fontweight='bold')
plt.show()