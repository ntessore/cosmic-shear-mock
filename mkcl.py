#!/usr/bin/env python

import numpy as np
import configparser

cfg = configparser.ConfigParser(inline_comment_prefixes=';#')

cfg.read('cosmosis.ini')

with open('flask.config') as f:
    flask_config = '[flask]\n' + f.read()
cfg.read_string(flask_config)

savedir = cfg.get('test', 'save_dir')

fields_info = cfg.get('flask', 'fields_info')
cl_prefix = cfg.get('flask', 'cl_prefix')
lmin, lmax = [int(i) for i in cfg.get('flask', 'lrange').split()]
lrange = np.arange(lmin, lmax+1)

info = np.loadtxt(fields_info)
nbin = len(info[info[:,0]==2])

ell = np.loadtxt(savedir + '/shear_cl/ell.txt')
for i, j in zip(*np.triu_indices(nbin)):
    cl = np.loadtxt(savedir + '/shear_cl/bin_{:}_{:}.txt'.format(j+1, i+1))
    out = np.transpose([lrange, np.interp(lrange, ell, cl)])
    np.savetxt(cl_prefix + 'f2z{:}f2z{:}.dat'.format(i+1, j+1), out)
