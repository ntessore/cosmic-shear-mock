import os, os.path
import numpy as np
import healpy as hp
from astropy.io import fits
from cosmosis.datablock import option_section
import configparser

def setup(options):
    nz_fits = options.get_string(option_section, 'nz_fits')
    fp_fits = options.get_string(option_section, 'fp_fits')
    config = options.get_string(option_section, 'config')

    with open(config) as f:
        flask_config = '[flask]\n' + f.read()
    cfg = configparser.ConfigParser(inline_comment_prefixes=';#')
    cfg.read_string(flask_config)

    cl_prefix = cfg.get('flask', 'cl_prefix')
    lmin, lmax = [int(i) for i in cfg.get('flask', 'lrange').split()]
    selec_prefix = cfg.get('flask', 'selec_prefix')
    selec_z_prefix = cfg.get('flask', 'selec_z_prefix')
    nside = cfg.getint('flask', 'nside')

    print('using flask config from', config)
    print('  cl_prefix:', cl_prefix)
    print('  lrange:', lmin, lmax)
    print('  selec_prefix:', selec_prefix)
    print('  selec_z_prefix:', selec_z_prefix)
    print('  nside:', nside)

    return nz_fits, fp_fits, cl_prefix, lmin, lmax, selec_prefix, selec_z_prefix, nside

def execute(block, config):
    nz_fits, fp_fits, cl_prefix, lmin, lmax, selec_prefix, selec_z_prefix, nside = config

    nbin = block['shear_cl', 'nbin']
    sample = block['shear_cl', 'sample_a']

    ell = block['shear_cl', 'ell']
    ell_out = np.arange(lmin, lmax+1)

    os.makedirs(os.path.dirname(cl_prefix), exist_ok=True)
    os.makedirs(os.path.dirname(selec_prefix), exist_ok=True)
    os.makedirs(os.path.dirname(selec_z_prefix), exist_ok=True)

    for i, j in zip(*np.triu_indices(nbin)):
        cl = block['shear_cl', 'bin_%d_%d' % (j+1, i+1)]
        name = '{:}f2z{:}f2z{:}.dat'.format(cl_prefix, i+1, j+1)
        data = np.transpose([ell_out, np.interp(ell_out, ell, cl)])
        np.savetxt(name, data)

    nz = fits.open(nz_fits)

    ng = []
    for i in range(nbin):
        ng.append(nz['nz_'+sample].header['NGAL_{:}'.format(i+1)])

    z = nz['nz_'+sample].data['Z_MID']
    f = []

    for row in nz['nz_'+sample].data:
        n = 0
        for i in range(nbin):
            n += row['BIN{:}'.format(i+1)]*ng[i]
        f.append(n)

    np.savetxt('{:}f1.dat'.format(selec_z_prefix), np.transpose([z, f]))

    fp = hp.read_map(fp_fits)
    fp = (fp > 0).astype(float)
    fp = hp.ud_grade(fp, nside)
    hp.write_map(selec_prefix, fp, overwrite=True)

    return 0

def cleanup(config):
    return 0
