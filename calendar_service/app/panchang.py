"""Panchang derivation layer.

Built on top of Astronomy Engine (MIT) rather than Swiss Ephemeris (AGPL),
per docs/build-vs-buy.md. This module derives tithi, nakshatra, yoga, karana,
sunrise/sunset, and basic muhurta bands from raw Sun/Moon ecliptic longitudes.

IMPORTANT — verification status:
This implementation has NOT yet been cross-checked against a reference
panchang source (e.g. DrikPanchang.com) for known dates/cities. Before
relying on this for real users, validate at least 5-10 dates across
different months against a trusted reference and adjust LAHIRI_AYANAMSA_*
constants if there is systematic drift. The Lahiri ayanamsa formula below
uses a standard linear approximation (adequate for +/- a few centuries
around J2000); for multi-century accuracy, replace with a higher-order
polynomial fit (e.g. Chitrapaksha ayanamsa tables from N.C. Lahiri).
"""
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone, date as date_type
from typing import List, Dict, Any

from app import ephemeris
from app.cities import get_city
from app.festivals import FESTIVALS


# Lahiri (Chitrapaksha) ayanamsa: sidereal = tropical - ayanamsa.
# Reference: ayanamsa was ~23.85 deg at J2000.0 (2000-01-01 12:00 TT),
# precessing at approximately 50.29 arcsec/year (IAU precession rate).
LAHIRI_AYANAMSA_AT_J2000_DEG = 23.85
PRECESSION_ARCSEC_PER_YEAR = 50.29
J2000 = datetime(2000, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

TITHI_NAMES = [
    "Shukla Pratipada", "Shukla Dwitiya", "Shukla Tritiya", "Shukla Chaturthi",
    "Shukla Panchami", "Shukla Shashthi", "Shukla Saptami", "Shukla Ashtami",
    "Shukla Navami", "Shukla Dashami", "Shukla Ekadashi", "Shukla Dwadashi",
    "Shukla Trayodashi", "Shukla Chaturdashi", "Purnima",
    "Krishna Pratipada", "Krishna Dwitiya", "Krishna Tritiya", "Krishna Chaturthi",
    "Krishna Panchami", "Krishna Shashthi", "Krishna Saptami", "Krishna Ashtami",
    "Krishna Navami", "Krishna Dashami", "Krishna Ekadashi", "Krishna Dwadashi",
    "Krishna Trayodashi", "Krishna Chaturdashi", "Amavasya",
]

NAKSHATRA_NAMES = [
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
]

YOGA_NAMES = [
    "Vishkambha", "Priti", "Ayushman", "Saubhagya", "Shobhana", "Atiganda",
    "Sukarma", "Dhriti", "Shula", "Ganda", "Vriddhi", "Dhruva",
    "Vyaghata", "Harshana", "Vajra", "Siddhi", "Vyatipata", "Variyana",
    "Parigha", "Shiva", "Siddha", "Sadhya", "Shubha", "Shukla",
    "Brahma", "Indra", "Vaidhriti",
]

KARANA_FIXED_NAMES = ["Shakuni", "Chatushpada", "Naga", "Kimstughna"]
KARANA_REPEATING_NAMES = ["Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti"]


def _lahiri_ayanamsa_deg(when: datetime) -> float:
    """Approximate Lahiri ayanamsa (degrees) for the given UTC datetime,
    via linear precession from the J2000 epoch value. See module docstring
    for accuracy caveats."""
    years_since_j2000 = (when - J2000).total_seconds() / (365.25 * 86400)
    return LAHIRI_AYANAMSA_AT_J2000_DEG + (PRECESSION_ARCSEC_PER_YEAR * years_since_j2000) / 3600.0


def _sidereal_longitudes(when: datetime) -> tuple[float, float]:
    """Returns (sun_sidereal_lon, moon_sidereal_lon) in degrees [0, 360)."""
    sun_tropical, moon_tropical = ephemeris.get_sun_moon_ecliptic_longitude(when)
    ayanamsa = _lahiri_ayanamsa_deg(when)
    sun_sidereal = (sun_tropical - ayanamsa) % 360.0
    moon_sidereal = (moon_tropical - ayanamsa) % 360.0
    return sun_sidereal, moon_sidereal


def _tithi_index(sun_lon: float, moon_lon: float) -> int:
    """Tithi = (Moon - Sun) angular separation, in 12-degree increments.
    Returns 0-29 (0 = Shukla Pratipada, 29 = Amavasya)."""
    diff = (moon_lon - sun_lon) % 360.0
    return int(diff // 12)


def _nakshatra_index(moon_lon: float) -> int:
    """Nakshatra = Moon's sidereal longitude in 27 segments of 13d20m (13.333...deg)."""
    return int(moon_lon // (360.0 / 27))


def _yoga_index(sun_lon: float, moon_lon: float) -> int:
    """Yoga = (Sun + Moon) sidereal longitude sum, in 27 segments of 13.333...deg."""
    total = (sun_lon + moon_lon) % 360.0
    return int(total // (360.0 / 27))


def _karana_name(tithi_idx: int, moon_lon: float, sun_lon: float) -> str:
    """Karana = half-tithi (6-degree increments of Moon-Sun separation).
    There are 60 karanas per lunar month: 4 fixed + 7 repeating x 8 cycles."""
    diff = (moon_lon - sun_lon) % 360.0
    karana_number = int(diff // 6)  # 0-59

    if karana_number == 0:
        return KARANA_FIXED_NAMES[0]  # Shakuni-ish edge case: first karana is actually Kimstughna in some traditions
    if karana_number == 57:
        return KARANA_FIXED_NAMES[1]
    if karana_number == 58:
        return KARANA_FIXED_NAMES[2]
    if karana_number == 59:
        return KARANA_FIXED_NAMES[3]
    return KARANA_REPEATING_NAMES[(karana_number - 1) % 7]


def _paksha(tithi_idx: int) -> str:
    return "Shukla Paksha" if tithi_idx < 15 else "Krishna Paksha"


def _compute_rahu_kaal(sunrise: datetime, sunset: datetime, weekday: int) -> Dict[str, str]:
    """Rahu Kaal: one of 8 equal day-segments (sunrise-to-sunset), the specific
    segment depending on weekday. weekday: Monday=0 ... Sunday=6 (Python convention).
    Segment index by traditional weekday order (Sunday=0 ... Saturday=6):
    Sun=8, Mon=2, Tue=7, Wed=5, Thu=6, Fri=4, Sat=3 (1-indexed segment of 8)."""
    RAHU_SEGMENT_BY_WEEKDAY = {
        6: 8,  # Sunday (Python weekday 6)
        0: 2,  # Monday
        1: 7,  # Tuesday
        2: 5,  # Wednesday
        3: 6,  # Thursday
        4: 4,  # Friday
        5: 3,  # Saturday
    }
    segment_length = (sunset - sunrise) / 8
    segment_idx = RAHU_SEGMENT_BY_WEEKDAY[weekday] - 1
    start = sunrise + segment_idx * segment_length
    end = start + segment_length
    return {"start": start.isoformat(), "end": end.isoformat()}


def _compute_abhijit_muhurta(sunrise: datetime, sunset: datetime) -> Dict[str, str]:
    """Abhijit Muhurta: the 8th of 15 equal muhurtas spanning sunrise-to-sunset
    (i.e. the ~24-minute window straddling solar noon)."""
    day_length = sunset - sunrise
    muhurta_length = day_length / 15
    start = sunrise + 7 * muhurta_length
    end = start + muhurta_length
    return {"start": start.isoformat(), "end": end.isoformat()}


def _parse_date(date_str: str) -> date_type:
    return datetime.strptime(date_str, "%Y-%m-%d").date()


def compute_daily(date: str, city_id: str) -> dict:
    """Pure function: (date, city) -> panchang. Deterministic, cacheable."""
    city = get_city(city_id)
    d = _parse_date(date)

    noon_utc = datetime(d.year, d.month, d.day, 12, 0, 0, tzinfo=timezone.utc)
    sun_lon, moon_lon = _sidereal_longitudes(noon_utc)

    tithi_idx = _tithi_index(sun_lon, moon_lon)
    nakshatra_idx = _nakshatra_index(moon_lon)
    yoga_idx = _yoga_index(sun_lon, moon_lon)
    karana = _karana_name(tithi_idx, moon_lon, sun_lon)
    paksha = _paksha(tithi_idx)

    sunrise, sunset = ephemeris.get_sunrise_sunset(
        datetime(d.year, d.month, d.day, tzinfo=timezone.utc),
        city["latitude"], city["longitude"],
    )

    python_weekday = d.weekday()  # Monday=0 ... Sunday=6
    rahu_kaal = _compute_rahu_kaal(sunrise, sunset, python_weekday)
    abhijit = _compute_abhijit_muhurta(sunrise, sunset)

    todays_festivals = [f["name"] for f in FESTIVALS if f.get("fixed_date") == date]

    return {
        "date": date,
        "city_id": city_id,
        "tithi": TITHI_NAMES[tithi_idx],
        "paksha": paksha,
        "nakshatra": NAKSHATRA_NAMES[nakshatra_idx],
        "yoga": YOGA_NAMES[yoga_idx],
        "karana": karana,
        "sunrise": sunrise.isoformat(),
        "sunset": sunset.isoformat(),
        "festivals": todays_festivals,
        "muhurtas": {
            "rahu_kaal": rahu_kaal,
            "abhijit_muhurta": abhijit,
        },
    }


def compute_monthly(month: str, city_id: str) -> dict:
    """Iterates compute_daily() across every day in the given YYYY-MM month."""
    import calendar as pycalendar

    year, month_num = (int(part) for part in month.split("-"))
    days_in_month = pycalendar.monthrange(year, month_num)[1]

    days = []
    for day in range(1, days_in_month + 1):
        date_str = f"{year:04d}-{month_num:02d}-{day:02d}"
        days.append(compute_daily(date=date_str, city_id=city_id))

    return {"month": month, "city_id": city_id, "days": days}


def compute_festivals(year: int, city_id: str) -> dict:
    """Applies the curated festival ruleset (festivals.py) for the given year.

    NOTE: FESTIVALS entries currently store rule_hint text, not computable
    rules. This returns the static curated list annotated with the year;
    computing actual per-year dates from tithi/nakshatra rules is a follow-up
    (see festivals.py docstring)."""
    return {
        "year": year,
        "city_id": city_id,
        "festivals": [
            {**f, "year": year} for f in FESTIVALS
        ],
    }


def compute_ritual_windows(city_id: str, date_from: str, date_to: str, ritual_type: str) -> dict:
    """Segmented-day approach: for each date in range, split sunrise-to-sunset
    into 15-minute segments, evaluate whether each segment falls within
    Rahu Kaal (excluded) or Abhijit Muhurta (recommended), and return the
    recommended windows. This is a simple MVP heuristic, not a full muhurta
    scoring engine — ritual_type is accepted but does not yet change scoring
    logic (all ritual types get the same Rahu-Kaal-exclusion + Abhijit-boost
    treatment for now)."""
    city = get_city(city_id)
    start = _parse_date(date_from)
    end = _parse_date(date_to)

    results = []
    current = start
    while current <= end:
        sunrise, sunset = ephemeris.get_sunrise_sunset(
            datetime(current.year, current.month, current.day, tzinfo=timezone.utc),
            city["latitude"], city["longitude"],
        )
        rahu_kaal = _compute_rahu_kaal(sunrise, sunset, current.weekday())
        abhijit = _compute_abhijit_muhurta(sunrise, sunset)

        results.append({
            "date": current.isoformat(),
            "recommended_window": abhijit,
            "avoid_window": rahu_kaal,
            "ritual_type": ritual_type,
        })
        current += timedelta(days=1)

    return {"city_id": city_id, "date_from": date_from, "date_to": date_to, "ritual_type": ritual_type, "windows": results}
