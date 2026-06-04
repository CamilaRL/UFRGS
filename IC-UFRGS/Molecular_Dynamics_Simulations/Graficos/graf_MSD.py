import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_msd = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\msd.txt"
teq, dr = np.loadtxt(endereco_msd, skiprows = 1, unpack = True)

# Ajuste
slope, intercept, rvalue, pvalue, stderr = stats.linregress(teq, dr)
dr_ajust = slope*teq + intercept
D = slope/(2*3)

# Grafico da MSD
#plt.plot(teq, dr_ajust, color='black', label=f'R^2: {rvalue}\nD: {D}')
plt.scatter(teq, dr, s=1)
plt.xlabel('Tempo')
plt.ylabel('MSD')
plt.title('Deslocamento Quadrático Médio', fontweight='bold')
#plt.legend()
plt.show()
