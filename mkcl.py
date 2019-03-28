#!/usr/bin/env python

import numpy as np
import configparser
import os

cfg = configparser.ConfigParser(inline_comment_prefixes=';#')

with open('flask.config') as f:
    flask_config = '[flask]\n' + f.read()
cfg.read_string(flask_config)

lmin, lmax = [int(i) for i in cfg.get('flask', 'lrange').split()]
lrange = np.arange(lmin, lmax+1)

print('flask lrange = {:}  {:}'.format(lmin, lmax))

info = np.loadtxt('input/flask-info.dat')
nbin = len(info[info[:,0]==2])

os.makedirs('data/flask', exist_ok=True)

ell = np.loadtxt('data/shear_cl/ell.txt')
for i, j in zip(*np.triu_indices(nbin)):
    cl = np.loadtxt('data/shear_cl/bin_{:}_{:}.txt'.format(j+1, i+1))
    out = np.transpose([lrange, np.interp(lrange, ell, cl)])
    np.savetxt('data/flask/cl-f2z{:}f2z{:}.dat'.format(i+1, j+1), out)
