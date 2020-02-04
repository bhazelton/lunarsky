
import numpy as np
import lunarsky.tests as ltest

from astropy.coordinates import ICRS, GCRS, EarthLocation, AltAz
from astropy.time import Time
import pytest

from lunarsky import MoonLocation, SkyCoord, LunarTopo, MCMF

# Check that the changes to SkyCoord don't cause unexpected behavior.


def test_skycoord_transforms():
    # An EarthLocation object should still get copied over
    # under transformations.

    eloc = EarthLocation.from_geodetic(0.0, 10.0)
    coords = ltest.get_catalog()

    altaz = coords.transform_to(AltAz(location=eloc, obstime=Time.now()))

    assert altaz.location == eloc

    gcrs = altaz.transform_to(GCRS())

    assert gcrs.location == eloc

    icrs = altaz.transform_to(ICRS())

    assert icrs.location == eloc


def test_skycoord_with_lunar_frames():
    # Check that defining a SkyCoord with frames
    # lunartopo and mcmf works correctly.

    Nsrcs = 10
    alts = np.random.uniform(0,np.pi/2., Nsrcs)
    azs = np.random.uniform(0, 2*np.pi, Nsrcs)

    loc = MoonLocation.from_selenodetic(0, 0)
    src = SkyCoord(alt = alts, az = azs, unit='rad', frame='lunartopo',
                   obstime=Time.now(), location=loc)

    assert src.location == loc
    assert isinstance(src.frame, LunarTopo)
    x, y, z = src.cartesian.xyz
    src2 = SkyCoord(x=x, y=y, z=z, frame='mcmf',
                   obstime=Time.now(), location=loc)

    assert isinstance(src2.frame, MCMF)
