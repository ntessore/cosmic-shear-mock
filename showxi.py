#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import configparser

cfg = configparser.ConfigParser(inline_comment_prefixes=';#')

cfg.read('cosmosis.ini')

with open('flask.config') as f:
    flask_config = '[flask]\n' + f.read()
cfg.read_string(flask_config)

savedir = cfg.get('test', 'save_dir')

fields_info = cfg.get('flask', 'fields_info')
xiout_prefix = cfg.get('flask', 'xiout_prefix')

info = np.loadtxt(fields_info)
nbin = len(info[info[:,0]==2])

for i, j in zip(*np.triu_indices(nbin)):
    th_cosmosis = np.degrees(np.loadtxt(savedir + '/shear_xi_plus/theta.txt'))
    xi_cosmosis = np.loadtxt(savedir + '/shear_xi_plus/bin_{:}_{:}.txt'.format(j+1, i+1))
    
    th_flask, xi_flask = np.transpose(np.loadtxt(xiout_prefix + 'f2z{:}f2z{:}.dat'.format(i+1, j+1)))

    plt.subplot(nbin, nbin, i*nbin+j+1)
    plt.plot(th_cosmosis, xi_cosmosis, '-', label='cosmosis')
    plt.plot(th_flask, xi_flask, '-', label='flask')
    plt.xlim(0.05, 50)
    plt.ylim(-0.1e-4, 1.1e-4)
    plt.yticks([])
    plt.semilogx()

plt.tight_layout()
#plt.legend()
plt.show()

