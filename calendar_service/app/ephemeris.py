"""Thin wrapper around the Astronomy Engine library.

Astronomy Engine (https://github.com/cosinekitty/astronomy) is MIT licensed
and provides Sun/Moon/planet geocentric positions used as raw inputs to the
panchang derivation layer in panchang.py. See docs/build-vs-buy.md for why
this was chosen over Swiss Ephemeris (AGPL-3.0).

PyPI package: astronomy-engine
Import name: astronomy
"""
from datetime import datetime, timezone
from typing import Tuple

import astronomy


def _to_astro_time(when: datetime) -> "astronomy.Time":
    """Converts a Python datetime (assumed or converted to UTC) to an
    astronomy.Time instance."""
    if when.tzinfo is None:
        when = when.replace(tzinfo=timezone.utc)
    when_utc = when.astimezone(timezone.utc)
    return astronomy.Time.Make(
        when_utc.year, when_utc.month, when_utc.day,
        when_utc.hour, when_utc.minute, when_utc.second,
    )


def get_sun_moon_ecliptic_longitude(when: datetime) -> Tuple[float, float]:
    """Returns (sun_ecliptic_longitude_deg, moon_ecliptic_longitude_deg),
    both geocentric apparent tropical ecliptic longitudes in degrees [0, 360).

    Used as the raw input for tithi/nakshatra/yoga derivation. Sidereal
    (Lahiri) correction is applied separately in panchang.py, not here —
    this function returns tropical longitudes only.
    """
    time = _to_astro_time(when)

    sun_vec = astronomy.GeoVector(astronomy.Body.Sun, time, aberration=True)
    sun_ecl = astronomy.Ecliptic(sun_vec)
    sun_lon = sun_ecl.elon % 360.0

    moon_vec = astronomy.GeoVector(astronomy.Body.Moon, time, aberration=True)
    moon_ecl = astronomy.Ecliptic(moon_vec)
    moon_lon = moon_ecl.elon % 360.0

    return sun_lon, moon_lon


def get_sunrise_sunset(when: datetime, observer_lat: float, observer_lon: float) -> Tuple[datetime, datetime]:
    """Returns (sunrise_utc, sunset_utc) for the given date and location.

    Uses astronomy-engine's SearchRiseSet, which accounts for standard
    atmospheric refraction internally.
    """
    time = _to_astro_time(when.replace(hour=0, minute=0, second=0, microsecond=0))
    observer = astronomy.Observer(observer_lat, observer_lon, 0)

    sunrise = astronomy.SearchRiseSet(astronomy.Body.Sun, observer, astronomy.Direction.Rise, time, 1)
    sunset = astronomy.SearchRiseSet(astronomy.Body.Sun, observer, astronomy.Direction.Set, time, 1)

    if sunrise is None or sunset is None:
        raise ValueError(
            f"Could not compute sunrise/sunset for lat={observer_lat}, lon={observer_lon} "
            f"on {when.date()} — likely a polar location/date with no rise or set event."
        )

    return sunrise.Utc(), sunset.Utc()
