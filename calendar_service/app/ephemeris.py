"""Thin wrapper around the Astronomy Engine library.

Astronomy Engine (https://github.com/cosinekitty/astronomy) is MIT licensed
and provides Sun/Moon/planet geocentric positions used as raw inputs to the
panchang derivation layer in panchang.py.

Install: pip install astronomy-engine
"""

def get_sun_moon_longitude(when, observer_lat: float, observer_lon: float):
    """Returns (sun_ecliptic_longitude_deg, moon_ecliptic_longitude_deg) for the given time/location.

    NOTE: Skeleton — wire up astronomy_engine.SunPosition / astronomy_engine.EquatorFromEcliptic
    (or equivalent current API) here once the dependency is installed and pinned.
    """
    raise NotImplementedError("Wire up astronomy-engine calls here.")


def get_sunrise_sunset(when, observer_lat: float, observer_lon: float):
    """Returns (sunrise_utc, sunset_utc) including atmospheric refraction."""
    raise NotImplementedError("Use astronomy_engine.SearchRiseSet or equivalent.")
