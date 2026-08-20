"""Panchang derivation layer.

Built on top of Astronomy Engine (MIT) rather than Swiss Ephemeris (AGPL),
per docs/build-vs-buy.md. This module derives tithi, nakshatra, yoga, karana,
sunrise/sunset, and Rahu Kaal from raw Sun/Moon ecliptic longitudes.

NOTE: Skeleton only. Full implementation requires:
  - Lahiri ayanamsa sidereal correction
  - Sun/Moon geocentric ecliptic longitude via astronomy-engine
  - Segmented-day muhurta window logic (sunrise-to-sunset split, excluding Rahu Kaal)
"""
from dataclasses import dataclass
from datetime import date as date_type


LAHIRI_AYANAMSA_EPOCH_OFFSET_DEG = 23.85  # placeholder reference value; verify against authoritative source before production use


@dataclass
class PanchangResult:
    date: str
    city_id: str
    tithi: str
    paksha: str
    nakshatra: str
    yoga: str
    karana: str
    sunrise: str
    sunset: str
    festivals: list
    muhurtas: dict


def compute_daily(date: str, city_id: str) -> dict:
    """Pure function: (date, city) -> panchang. Deterministic, cacheable."""
    raise NotImplementedError(
        "Implement using astronomy-engine Sun/Moon longitude calls + Lahiri ayanamsa offset. "
        "See docs/build-vs-buy.md for engine rationale."
    )


def compute_monthly(month: str, city_id: str) -> dict:
    raise NotImplementedError("Iterate compute_daily() across the month's dates.")


def compute_festivals(year: int, city_id: str) -> dict:
    raise NotImplementedError("Apply curated festival ruleset (see festivals.py) against computed tithi/nakshatra data.")


def compute_ritual_windows(city_id: str, date_from: str, date_to: str, ritual_type: str) -> dict:
    raise NotImplementedError(
        "Segmented-day approach: split sunrise-to-sunset into fixed segments, "
        "evaluate panchang at segment midpoints, exclude Rahu Kaal, return recommended windows."
    )
