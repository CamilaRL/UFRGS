from sympy import symbols, lambdify, exp
import numpy as np
import matplotlib.pyplot as plt


n_points = 1000
sig = 1.0
a = 5
b = -0.25
c = 1.0
d = 0.5
r0 = 0.7
r1 = 3.0
ri = 0.05
rf = 5
rc = 4.5*sig

r = symbols('r', real=True)
pot0 = 4*((sig/rc)**12 - (sig/rc)**6) + a*exp(-(1/(c**2))*((rc-r0)/sig)**2) + b*exp(-(1/(d**2))*((rc-r1)/sig)**2)
pot = 4*((sig/r)**12 - (sig/r)**6) + a*exp(-(1/(c**2))*((r-r0)/sig)**2) + b*exp(-(1/(d**2))*((r-r1)/sig)**2) - pot0
force = -pot.diff(r)

lamb_pot = lambdify(r, pot)
lamb_force = lambdify(r, force)

points = np.linspace(ri, rf, n_points)

y1 = lamb_pot(points)
y2 = lamb_force(points)

'''
plt.figure(figsize=(10,5))
plt.subplot(121)
plt.scatter(points, y1, s=1)
plt.ylabel('Potential')
plt.xlabel('r')

plt.subplot(122)
plt.scatter(points, y2, s=1)
plt.ylabel('Force')
plt.xlabel('r')

plt.tight_layout()
plt.show()
'''

f =  open('./force.table', 'w')

f.write('AA\n')
f.write(f"N {n_points} R {ri} {rf}\n\n")

for i in range(n_points):
    f.write(f'{i+1} {points[i]} {y1[i]} {y2[i]}\n')

f.write('\n')
f.close()