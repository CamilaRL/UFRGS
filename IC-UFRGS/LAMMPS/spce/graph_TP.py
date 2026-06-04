import matplotlib.pyplot as plt
import numpy as np

T, P = np.loadtxt('./isoline/rho1.05/harmonic-test/meanFile.txt', unpack=True)
T1, P1 = np.loadtxt('./isoline/rho1.05/harmonic-test/meanFile-short.txt', unpack=True, comments="#")
#T2, P2 = np.loadtxt('./isoline/rho1.10/meanFile.txt', unpack=True)

# Transformar em Mega Pascal    
P = P*101325/(10**6)
P1 = P1*101325/(10**6)
#P2 = P2*101325/(10**6)

plt.scatter(T1, P1, marker='.', color='black', label=r'Short Time - $\rho$ = 1.05 g/cm^3')
plt.plot(T1, P1, color='black', linewidth=0.5)
#plt.scatter(T2, P2, marker='^', color='black', label=r'Zero Bounds - $\rho$ = 1.10 g/cm^3')
#plt.plot(T2, P2, color='black', linewidth=0.5)
plt.scatter(T, P, marker='.', color='blue', label=r'Longer Time - $\rho$ = 1.05 g/cm^3')
plt.plot(T, P, color='blue', linewidth=0.5)
plt.ylabel('P (MPa)')
plt.xlabel('T (K)')
plt.legend()
plt.ylim(bottom=0)
plt.show()