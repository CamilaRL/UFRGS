import numpy as np
import matplotlib.pyplot as plt

s = 1000000
Nc = np.zeros(s)
nqc = np.zeros(s)
ncc = np.zeros(s)
xc = np.zeros(s)
yc = np.zeros(s)

Ns = np.zeros(s)
nqs = np.zeros(s)
ncs = np.zeros(s)
xs = np.zeros(s)
ys = np.zeros(s)

for i in range(1,3):
    Nc_samp, nqc_samp, ncc_samp, xc_samp, yc_samp = np.loadtxt(f'./sample{i}/cr.txt', unpack=True, skiprows=2)
    Ns_samp, nqs_samp, ncs_samp, xs_samp, ys_samp = np.loadtxt(f'./sample{i}/sr.txt', unpack=True, skiprows=2)

    for j in range(len(Nc_samp)):

        Nc[j] = Nc[j] + Nc_samp[j]
        nqc[j] = nqc[j] + nqc_samp[j]
        ncc[j] = ncc[j] + ncc_samp[j]
        xc[j] = xc[j] + xc_samp[j]
        yc[j] = yc[j] + yc_samp[j]

        Ns[j] = Ns[j] + Ns_samp[j]
        nqs[j] = nqs[j] + nqs_samp[j]
        ncs[j] = ncs[j] + ncs_samp[j]
        xs[j] = xs[j] + xs_samp[j]
        ys[j] = ys[j] + ys_samp[j]


Nc = Nc/3
nqc = nqc/3
ncc = ncc/3
xc = xc/3
yc = yc/3

Ns = Ns/3
nqs = nqs/3
ncs = ncs/3
xs = xs/3
ys = ys/3


nNc = ncc/nqc
nNs = ncs/nqs

plt.plot(Nc[1000:], nNc[1000:], label='Com Rejeição')
plt.plot(Ns[1000:], nNs[1000:], label='Sem Rejeição')
plt.axhline(y = np.pi/4, color = 'k', linestyle = '-', label=r'$\frac{\pi}{4}$')
plt.ylabel('n/N')
plt.xlabel('N')
plt.legend()
plt.show()
