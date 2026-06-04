import numpy as np
import matplotlib.pyplot as plt

# Importa dados
pasta = input('Insira a pasta dos resultados: ')
endereco_v = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC_Fluidos\\Programas\\Simulacoes\\{pasta}\\velocidades9900.txt"
vx, vy, vz = np.loadtxt(endereco_v, skiprows = 1, unpack = True)

endereco_x = f"C:\\Users\\camil\\Desktop\\UFRGS\\IC-Fluidos\\Programas\\Simulacoes\\{pasta}\\Posicoes\\pos9900.txt"
x, y, z = np.loadtxt(endereco_x, skiprows = 2, usecols= (1,2,3), unpack = True)

b = 15

v = list(np.sqrt(vx[i]**2 + vy[i]**2 + vz[i]**2) for i in range(len(vx)))
pos = list(np.sqrt(x[i]**2 + y[i]**2 + z[i]**2) for i in range(len(x)))

# Graficos da temperatura
fig = plt.figure(figsize=(10,5))
plt.subplot(241)
plt.hist(v, b)
plt.xlabel('Velocidades')
plt.ylabel('Frequencia')
plt.title('Direção x')

plt.subplot(245)
plt.scatter(x, vx, s=1)
plt.xlabel('Posição')
plt.ylabel('Velocidades')

plt.subplot(242)
plt.hist(vy, b)
plt.xlabel('Velocidades')
#plt.ylabel('Frequencia')
plt.title('Direção y')

plt.subplot(246)
plt.scatter(y, vy, s=1)
plt.xlabel('Posição')
#plt.ylabel('Velocidades')

plt.subplot(243)
plt.hist(vz, b)
plt.xlabel('Velocidades')
#plt.ylabel('Frequencia')
plt.title('Direção z')

plt.subplot(247)
plt.scatter(z, vz, s=1)
plt.xlabel('Posição')
#plt.ylabel('Velocidades')

plt.subplot(244)
plt.hist(v, b)
plt.xlabel('Velocidades')
plt.title('Vetor')

plt.subplot(248)
plt.scatter(pos, v, s=1)
plt.xlabel('Posição')

plt.suptitle('Distribuição de velocidades')
plt.subplots_adjust(hspace=0.4, wspace=0.3)
plt.show()