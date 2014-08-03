import numpy
from . import _healpix

def eq2ang(ra, dec):
    """
    convert equatorial ra,dec in degrees to angular theta, phi in radians

    theta = pi/2-dec*D2R
    phi = ra*D2R

    parameters
    ----------
    ra: scalar or array
        Right ascension in degrees
    dec: scalar or array
        Declination in degrees

    returns
    -------
    theta: scalar or array
        pi/2-dec*D2R
    phi: scalar or array
        phi = ra*D2R
    """
    theta = numpy.deg2rad(dec)
    theta *= -1
    theta += (0.5*numpy.pi)
    phi = numpy.deg2rad(ra)

    return theta, phi

class HealPix(_healpix.HealPix):
    """
    class representing a healpix resolution

    parameters
    ----------
    nside: int
        healpix resolution

    attributes
    ----------
    nside
    npix
    ncap
    area

    methods
    -------
    hp=HealPix(nside)
    pixnum=hp.eq2pix(ra, dec) 

    # these are the same as the read only attributes above
    get_nside()
    get_npix()
    get_ncap()
    get_area()
    """

    def eq2pix(self, ra, dec, scheme='ring'):
        """
        get the pixel number(s) for the input ra,dec

        parameters
        ----------
        ra: scalar or array
            right ascension
        dec: scalar or array
            declination
        scheme: string
            'ring' or 'nest'.  Only ring supported currently

        returns
        -------
        pixnum: scalar array
            The pixel number(s)
        """

        if scheme != 'ring':
            raise ValueError("only ring scheme is currently supported")

        is_scalar=numpy.isscalar(ra)

        ra  = numpy.array(ra, dtype='f8', ndmin=1, copy=False)
        dec = numpy.array(dec, dtype='f8', ndmin=1, copy=False)

        if ra.size != dec.size:
            raise ValueError("ra,dec must have same size, "
                             "got %s,%s" % (ra.size,dec.size))
        pixnum = numpy.zeros(ra.size, dtype='i8')

        super(HealPix,self)._fill_eq2pix_ring(ra, dec, pixnum)

        if is_scalar:
            pixnum=pixnum[0]
        return pixnum
