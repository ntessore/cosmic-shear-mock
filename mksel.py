#!/usr/bin/env python

import numpy as np
import healpy as hp
from astropy.io import fits
import configparser

cfg = configparser.ConfigParser(inline_comment_prefixes=';#')

cfg.read('cosmosis.ini')

with open('flask.config') as f:
    flask_config = '[flask]\n' + f.read()
cfg.read_string(flask_config)

nz_file = cfg.get('load_nz', 'nz_file')
dataset = 'nz_' + cfg.get('load_nz', 'data_sets')

nside = cfg.getint('flask', 'nside')

info = np.loadtxt('input/flask-info.dat')
nbin = len(info[info[:,0]==2])

nz = fits.open(nz_file)

ng = []
for i in range(nbin):
    ng.append(nz[dataset].header['NGAL_{:}'.format(i+1)])

z = nz[dataset].data['Z_MID']
f = []

for row in nz[dataset].data:
    n = 0
    for i in range(nbin):
        n += row['BIN{:}'.format(i+1)]*ng[i]
    f.append(n)

np.savetxt('data/flask/fz-f1.dat', np.transpose([z, f]))

dat = hp.read_map('input/survey_footprint.fits')
dat = (dat > 0).astype(float)
dat = hp.ud_grade(dat, nside)
hp.write_map('data/flask/sel.fits', dat, overwrite=True)
