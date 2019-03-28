# mock cosmic shear catalogues

This is a simple toolchain to generate mock cosmic shear catalogues using
the [CosmoSIS] test sampler and a pseudomodule to generate [FLASK] input data.

    $ cosmosis cosmosis.ini     # run CosmoSIS to generate FLASK data
    $ flask flask.config        # run FLASK to generate the mock catalogue

The process is configured through the following files.

-   `cosmosis.ini` -- CosmoSIS configuration file.

    Set the basic simulation parameters such as number of Cls etc. here. Also
    contains the source redshift distribution, survey footprint, and name of
    FLASK config file to use.

-   `flask.config` -- FLASK configuration file.

    Set the basic random field synthesis parameters here. Important parameters
    are maximum ell for Cls (small scale cutoff) and size of the random field
    map. This file is also read by the CosmoSIS pseudomodule.

-   `values.ini` -- Cosmological parameter values.

    Set the cosmology here.

-   `fields.dat` -- FLASK field information.

    This file contains the tomographic redshift bin information for the mock
    shear catalogue. It must contain a galaxy field (1) and a shear field (2).

[CosmoSIS]: https://bitbucket.org/joezuntz/cosmosis/
[FLASK]: http://www.astro.iag.usp.br/~flask/

