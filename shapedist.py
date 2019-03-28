#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import RectBivariateSpline

def clvl(aa, ll):
    al, ah = aa.min(), aa.max()
    uu = np.linspace(al, ah, 100)
    vv = np.array([aa[aa <= u].sum() for u in uu])
    vv = vv/aa.sum()
    return np.interp(ll, vv, uu)

ra, dec, e1, e2, w = np.loadtxt('catalog/shear_1.txt').T

x1, x2 = np.sqrt(w)*e1, np.sqrt(w)*e2

q = np.mean([x1**2, x2**2], axis=None)
k = np.mean([x1**4, x2**4], axis=None)/q**2

print('q = ', q)
print('k = ', k)

nn, b1, b2 = np.histogram2d(x1, x2, range=[[-5, 5], [-5, 5]], bins=50)

fn = RectBivariateSpline((b1[:-1] + b1[1:])/2, (b2[:-1] + b2[1:])/2,
                         nn, bbox=[-5, 5, -5, 5], kx=1, ky=1, s=0)

u = np.linspace(-5, 5, 1000)
u1, u2 = u[np.newaxis,:], u[:,np.newaxis]

NN = fn(u1, u2)
NN = NN/np.trapz(np.trapz(NN, u), u)

FF = np.exp(-0.5*np.hypot(u1, u2)**2)
FF = FF/np.trapz(np.trapz(FF, u), u)

cl = clvl(NN, [0.01, 0.05, 0.32])
cl2 = clvl(FF, [0.01, 0.05, 0.32, 1])

fig = plt.figure(figsize=(4, 4))

grid = plt.GridSpec(5, 5, hspace=0.0, wspace=0.0)

ax1 = fig.add_subplot(grid[1:, :-1], xticks=[-4, -2, 0, 2, 4], yticks=[-4, -2, 0, 2, 4])
ax2 = fig.add_subplot(grid[1:, -1], xticks=[], sharey=ax1)
ax3 = fig.add_subplot(grid[0, :-1], yticks=[], sharex=ax1)

ax1.set_xlabel(r'$\sqrt{w} \; \epsilon_1$')
ax1.set_ylabel(r'$\sqrt{w} \; \epsilon_2$')

ax1.axhline(0, c='grey', lw=0.5, alpha=0.5, zorder=-1)
ax1.axvline(0, c='grey', lw=0.5, alpha=0.5, zorder=-1)
ax2.axhline(0, c='grey', lw=0.5, alpha=0.5, zorder=-1)
ax3.axvline(0, c='grey', lw=0.5, alpha=0.5, zorder=-1)

ax1.contour(u, u, NN, cl, colors='k')
ax1.contour(u, u, FF, cl2, colors='r', linestyles='dotted')

ax2.plot(np.trapz(NN, u, axis=0), u, c='k')
ax2.plot(np.trapz(FF, u, axis=0), u, c='r', ls='dotted')

ax3.plot(u, np.trapz(NN, u, axis=1), c='k')
ax3.plot(u, np.trapz(FF, u, axis=1), c='r', ls='dotted')

plt.show()
