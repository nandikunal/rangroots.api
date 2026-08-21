"""FastAPI entrypoint for the Calendar & Muhurta service.

Stateless service: given (date, city/lat-long, timezone) -> panchang result.
Built on Astronomy Engine (MIT license), not Swiss Ephemeris (AGPL).
"""
from fastapi import FastAPI
from app.schemas import DailyPanchangResponse
from app import panchang

app = FastAPI(title="Rang Roots Calendar Service", version="0.1.0")


@app.get("/api/calendar/daily", response_model=DailyPanchangResponse)
def get_daily_panchang(date: str, city_id: str):
    """Returns tithi, paksha, sunrise/sunset, main festivals, basic muhurta bands."""
    return panchang.compute_daily(date=date, city_id=city_id)


@app.get("/api/calendar/monthly")
def get_monthly_panchang(month: str, city_id: str):
    """Returns list of days with key panchang info and festivals for the month."""
    return panchang.compute_monthly(month=month, city_id=city_id)


@app.get("/api/calendar/festivals")
def get_festivals(year: int, city_id: str):
    """Returns major festivals for the year with computed local dates."""
    return panchang.compute_festivals(year=year, city_id=city_id)


@app.post("/api/calendar/ritual-muhurta")
def get_ritual_muhurta(city_id: str, date_from: str, date_to: str, ritual_type: str):
    """Segmented-day muhurta recommendation for a ritual type over a date range."""
    return panchang.compute_ritual_windows(
        city_id=city_id, date_from=date_from, date_to=date_to, ritual_type=ritual_type
    )
