import matplotlib.pyplot as plt
import numpy as np

def circulo(x):
    return np.sqrt(1-x**2)



x_list = np.linspace(0, 1, 100)
y = circulo(x_list)

Nc, nqc, ncc, xc, yc = np.loadtxt('./sample1/cr.txt', unpack=True, skiprows=2)
Ns, nqs, ncs, xs, ys = np.loadtxt('./sample1/sr.txt', unpack=True, skiprows=2)


#############
'''
fig = plt.figure(figsize=(10,5))

plt.subplot(121)
#plt.plot(x_list, y)
plt.scatter(xc, yc, s=0.5)
plt.plot(xc, yc)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Com Rejeição')
#plt.xlim(right=1, left=0)
#plt.ylim(bottom=0, top=1)

plt.subplot(122)
#plt.plot(x_list,y)
plt.scatter(xs, ys, s=0.5)
plt.plot(xs, ys)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Sem Rejeição')

plt.show()
'''

#############

nNc = ncc/nqc
nNs = ncs/nqs

plt.plot(Nc[1000:], nNc[1000:], label='Com Rejeição')
plt.plot(Ns[1000:], nNs[1000:], label='Sem Rejeição')
plt.axhline(y = np.pi/4, color = 'k', linestyle = '-', label=r'$\frac{\pi}{4}$')
plt.ylabel('n/N')
plt.xlabel('N')
plt.legend()
plt.show()

#############

'''

hist_c = list(int(x/0.01) for x in xc)
hist_s = list(int(x/0.01) for x in xs)

fig = plt.figure(figsize=(10,5))

plt.subplot(121)
plt.hist(hist_c, bins=100)
plt.xlabel('x')
plt.ylabel('Frequência')
plt.title('Com Rejeição')

plt.subplot(122)
plt.hist(hist_s, bins=100)
plt.xlabel('x')
plt.ylabel('Frequência')
plt.title('Sem Rejeição')

plt.show()'''

