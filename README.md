# mock cosmic shear catalogues

This is a simple pipeline to generate mock cosmic shear catalogues using
[CosmoSIS] and [FLASK]. The process is roughly as follows.

    $ cosmosis cosmosis.ini     # run CosmoSIS to generate Cls
    $ ./mkcl.py                 # convert Cls to FLASK format
    $ ./mksel.py                # generate FLASK's selection function
    $ flask flask.config        # run FLASK to generate the mock catalogue
    $ ./showxi.py               # make sure xi from CosmoSIS and FLASK matches
    $ ./mkcat.py                # generate the cosmic shear catalogues
    $ ./shapedist.py            # check the catalogue's shape distribution

The pipeline is configured through the following files, from which all other
data is generated.

-   `cosmosis.ini` -- CosmoSIS configuration file.

    Set the basic cosmology simulation parameters such as number of Cls etc.
    here. Also contains the source redshift distribution n(z) of the catalogue,
    which must be in the FITS standard format.

-   `flask.config` -- FLASK configuration file.

    Set the basic random field synthesis parameters here. Important parameters
    are maximum ell for Cls (small scale cutoff) and size of the random field
    map.

-   `input/cosmosis-values.ini` -- Cosmological parameter values.

    Set the cosmology here.

-   `input/flask-info.dat` -- FLASK field information.

    This file contains the tomographic redshift bin information for the mock
    shear catalogue. It must contain a galaxy field (1) and a shear field (2).

-   `input/survey-footprint.fits` -- Binary survey footprint map.

    Binary HEALPix map that contains the survey footprint. It is automatically
    resampled to match the map size in `flask.config` by the `mksel.py` tool.
    This should be a symlink to your survey data.

[CosmoSIS]: https://bitbucket.org/joezuntz/cosmosis/
[FLASK]: http://www.astro.iag.usp.br/~flask/

