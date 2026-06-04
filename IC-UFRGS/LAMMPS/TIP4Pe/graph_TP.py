import matplotlib.pyplot as plt
import numpy as np

#file = input('Arquivo das médias: ')
#file = './implicit/meanFile.txt'
file = './implicit100/TPdata.txt'
T, P = np.loadtxt(file, unpack=True, usecols=(0,1))
#T1, P1 = np.loadtxt('./implicit/tp-raul.txt', unpack=True, comments="#", usecols=(0,1))
T1, P1 = np.loadtxt('./rogelma/nve/meanFile.txt', unpack=True, usecols=(0,1))

# Transformar em Mega Pascal    
'''P = P*101325/(10**6)
#P1 = P1*101325/(10**6)
#P2 = P2*101325/(10**6)
'''
# Transformar em Kilo Bar
P = P*1.01325/1000
P1 = P1*1.01325/1000


plt.scatter(T1[:], P1[:], color='blue', label=r'$\rho_{500}$ = 1.05 g/$cm^3$')
plt.plot(T1[:], P1[:], color='blue', linewidth=0.8)
#plt.scatter(T2, P2, marker='^', color='black', label=r'- $\rho$ = 1.10 g/cm^3')
#plt.plot(T2, P2, color='black', linewidth=0.5)
plt.scatter(T[:], P[:], color='black', label=r'$\rho_{100}$ = 1.05 g/$cm^3$')
plt.plot(T[:], P[:], color='black', linewidth=0.8)
plt.ylabel('P (Kbar)', fontsize=12)
plt.xlabel('T (K)', fontsize=12)
plt.legend()
plt.title('Diagrama de Fase', fontsize=16)
plt.ylim(bottom=0)
plt.show()

'''

fig, ax1 = plt.subplots()

ax1.plot(T1[:], P1[:], color='blue', linewidth=0.8)
ax1.scatter(T1[:], P1[:], color='blue', label=r'$\rho_{ref}$ = 1.05 g/$cm^3$')
ax1.set_xlabel('T (K)', fontsize=12)
ax1.set_ylabel(r'$P_{ref}$ (Kbar)', fontsize=12, color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.set_ylim(0.55, 2.)

ax2 = ax1.twinx()

ax2.plot(T[11:], P[11:], color='purple', linewidth=0.8)
ax2.scatter(T[11:], P[11:], color='purple', label=r'$\rho$ = 1.05 g/$cm^3$')
ax2.set_ylabel('P (Kbar)', fontsize=12, color='purple')
ax2.tick_params(axis='y', labelcolor='purple')
ax2.set_ylim(0.7, 1.4)

plt.title(r'Diagrama de Fase - $\rho$ = 1.05 g/$cm^3$', fontsize=16)
fig.tight_layout()
plt.show()
'''