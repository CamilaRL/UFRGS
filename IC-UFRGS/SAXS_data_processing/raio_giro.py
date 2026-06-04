import numpy as np
import matplotlib.pyplot as plt

with open('absolute_butanol.dat', 'r') as arq:
    q, I, sI = np.loadtxt(arq, unpack='True')

#remove valores negativos de I, pois são inválidos para log
Ipos = np.delete(I, np.where(I <= 0))
qpos = np.delete(q, np.where(I <= 0))

q2 = qpos**2
lnI = np.log(Ipos)
I1 = 1/Ipos

#seleciona intervalo para realizar ajustes
q2_min = 0.006
q2_max = 0.018
i = np.where((q2 > q2_min) & (q2 < q2_max))
q2_ajuste = q2[i]
lnI_ajuste = lnI[i]
I1_ajuste = I1[i]

coef_g = np.polyfit(q2_ajuste, lnI_ajuste, 1)
Ag, Bg = coef_g[0], coef_g[1]
coef_o = np.polyfit(q2_ajuste, I1_ajuste, 1)
Ao, Bo = coef_o[0], coef_o[1]

print(f'\nAjuste de Guinier: \nA = {Ag} e B = {Bg}')
print(f'Raio de Giro = {np.sqrt(-3*Ag)} \nIntensidade a 0 = {np.exp(Bg)}')
print(f'\nAjuste de Ornstein-Zernike: \nA = {Ao} e B = {Bo}')
print(f'Raio de Giro = {np.sqrt(3*Ao/Bo)} \nIntensidade a 0 = {1/Bo}\n')

plt.scatter(q2, lnI, s=5)
plt.xlabel(r'$q^2$')
plt.ylabel(r'$\ln{I}$')
plt.title('Gráfico para ajuste de Guinier')
plt.show()

plt.scatter(q2, I1, s=5)
plt.xlabel(r'$q^2$')
plt.ylabel(r'$I^{-1}$')
plt.title('Gráfico para ajuste de Ornstein-Zernike')
plt.show()

plt.scatter(q2_ajuste, lnI_ajuste, s=5)
plt.plot(q2_ajuste, q2_ajuste*coef_g[0] + coef_g[1], 'b')
plt.xlabel(r'$q^2$')
plt.ylabel(r'$\ln{I}$')
plt.title('Ajuste de Guinier')
plt.show()

plt.scatter(q2_ajuste, I1_ajuste, s=5)
plt.plot(q2_ajuste, q2_ajuste*coef_o[0] + coef_o[1], 'b')
plt.xlabel(r'$q^2$')
plt.ylabel(r'$I^{-1}$')
plt.title('Ajuste de Ornstein-Zernike')
plt.show()