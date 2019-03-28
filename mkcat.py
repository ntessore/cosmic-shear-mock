#!/usr/bin/env python

import numpy as np
import configparser

cfg = configparser.ConfigParser(inline_comment_prefixes=';#')

with open('flask.config') as f:
    flask_config = '[flask]\n' + f.read()
cfg.read_string(flask_config)

fields_info = cfg.get('flask', 'fields_info')
ellip_sigma = cfg.getfloat('flask', 'ellip_sigma')
catalog_out = cfg.get('flask', 'catalog_out')
catalog_cols = cfg.get('flask', 'catalog_cols').split()

info = np.loadtxt(fields_info)
bins = info[info[:,0] == 2,-2:]

cat = np.loadtxt(catalog_out)

n = len(cat)

ra = cat[:, catalog_cols.index('ra')]
dec = cat[:, catalog_cols.index('dec')]
z = cat[:, catalog_cols.index('z')]
e1 = cat[:, catalog_cols.index('ellip1')]
e2 = cat[:, catalog_cols.index('ellip2')]

w = np.ones(n)/(ellip_sigma*ellip_sigma)

print('input catalog size: {:}'.format(n))

cat = np.transpose([ra, dec, e1, e2, w])

n = 0
for i, b in enumerate(bins):
    sel = np.where((z >= b[0]) & (z < b[1]))
    c = sel[0].size
    print('bin {:} = [{:.4f}, {:.4f}) size {:}'.format(i+1, *b, c))
    np.savetxt('catalog/shear_{:}.txt'.format(i+1), cat[sel])
    n += c

print('output catalog size: {:}'.format(n))
