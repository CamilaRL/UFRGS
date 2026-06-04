import numpy as np
import matplotlib.pyplot as plt

# Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_T = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\temperaturas.txt"
t, T = np.loadtxt(endereco_T, skiprows = 1, unpack = True)

# Graficos da temperatura
plt.scatter(t, T, s=0.1)
plt.xlabel('Tempo')
plt.ylabel('Temperatura')
plt.title('Evolução da temperatura do sistema')
plt.grid(True)
plt.show()