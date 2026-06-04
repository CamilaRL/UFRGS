from sympy import symbols, lambdify, exp
import numpy as np
import matplotlib.pyplot as plt



def lj(sig, e, r):
    return 4*e*((sig/r)**12 - (sig/r)**6)

def cs(sig, e, r, u0, u1, c0, c1, r0, r1):
    return lj(sig, e, r) + u0*e*exp(-(1/(c0**2))*((r-r0)/sig)**2) + u1*e*exp(-(1/(c1**2))*((r-r1)/sig)**2)


# variaveis para a tabela de forca
n_points = 1000
ri = 0.005
rf = 5
y_Usc = []
y_Ulj = []
y_Uwca = []
y_Fsc = []
y_Flj = []
y_Fwca = []


r = symbols('r', real=True)

# Potencial core-softened
sigAA = 1.0
eAA = 1.0
u0 = 5.0
u1 = -0.75
c0 = 1
c1 = 0.5
r0 = 0.7*sigAA
r1 = 2.5*sigAA

rc = (2**(1/6))*sigAA

U0 = cs(sigAA, eAA, rc, u0, u1, c0, c1, r0, r1)
U_sc = cs(sigAA, eAA, r, u0, u1, c0, c1, r0, r1)

force_sc = -U_sc.diff(r)

lamb_U_sc = lambdify(r, U_sc)
lamb_force_sc = lambdify(r, force_sc)

# Potencial Lennard-Jones

sigAB = 2.5
eAB = 1.1 # outros casos: 1.1 e 1.3
rc = (2**(1/6))*sigAB

U0 = lj(sigAB, eAB, rc)
U_lj = lj(sigAB, eAB, r)

force_lj = -U_lj.diff(r)

lamb_U_lj = lambdify(r, U_lj)
lamb_force_lj = lambdify(r, force_lj)

# Potencial WCA
sigBB = 2.5
eBB = 1.2
rc = (2**(1/6))*sigBB

U0 = lj(sigBB, eBB, rc)
U_wca = lj(sigBB, eBB, r) - U0

force_wca = -U_wca.diff(r)

lamb_U_wca = lambdify(r, U_wca)
lamb_force_wca = lambdify(r, force_wca)


### Calculo dos valores da tabela

points = np.linspace(ri, rf, n_points)

    # Potencial A-A
y_Usc = lamb_U_sc(points)
y_Fsc = lamb_force_sc(points)

    # Potencial A-B
y_Ulj = lamb_U_lj(points)
y_Flj = lamb_force_lj(points)

    # Potencial B-B
for i in range(len(points)):
    if(points[i] > rc):
        y_Uwca.append(0)
        y_Fwca.append(0)
    else:
        y_Uwca.append(lamb_U_wca(points[i]))
        y_Fwca.append(lamb_force_wca(points[i]))

### Arquivo

f =  open('./force.table', 'w')

# Potencial SC
f.write('AA\n')
f.write(f"N {n_points} R {ri} {rf}\n\n")

for i in range(n_points):
    f.write(f'{i+1} {points[i]} {y_Usc[i]} {y_Fsc[i]}\n')

# Potencial LJ
f.write('\nAB\n')
f.write(f"N {n_points} R {ri} {rf}\n\n")

for i in range(n_points):
    f.write(f'{i+1} {points[i]} {y_Ulj[i]} {y_Flj[i]}\n')

# Potencial WCA
f.write('\nBB\n')
f.write(f"N {n_points} R {ri} {rf}\n\n")

for i in range(n_points):
    f.write(f'{i+1} {points[i]} {y_Uwca[i]} {y_Fwca[i]}\n')

f.write('\n')
f.close()