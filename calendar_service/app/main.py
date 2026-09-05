"""FastAPI entrypoint for the Calendar & Muhurta service.

Stateless service: given (date, city/lat-long, timezone) -> panchang result.
Built on Astronomy Engine (MIT license), not Swiss Ephemeris (AGPL).
"""
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.schemas import CalendarHighlightsResponse, DailyPanchangResponse, FestivalsResponse, MonthlyPanchangResponse, ResolvedLocationResponse
from app import panchang

app = FastAPI(title="Rang Roots Calendar Service", version="0.1.0")

allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/calendar/daily", response_model=DailyPanchangResponse)
def get_daily_panchang(date: str, city_id: str | None = None, lat: float | None = None, lng: float | None = None):
    """Returns tithi, paksha, sunrise/sunset, main festivals, basic muhurta bands.

    Supports either a city_id lookup or direct lat/lng coordinates for location-aware use cases.
    """
    if city_id is None and (lat is None or lng is None):
        raise HTTPException(status_code=400, detail="Provide city_id or both lat and lng")
    return panchang.compute_daily(date=date, city_id=city_id, lat=lat, lng=lng)


@app.get("/api/calendar/monthly", response_model=MonthlyPanchangResponse)
def get_monthly_panchang(month: str, city_id: str | None = None, lat: float | None = None, lng: float | None = None):
    """Returns list of days with key panchang info and festivals for the month."""
    if city_id is None and (lat is None or lng is None):
        raise HTTPException(status_code=400, detail="Provide city_id or both lat and lng")
    return panchang.compute_monthly(month=month, city_id=city_id, lat=lat, lng=lng)


@app.get("/api/calendar/festivals", response_model=FestivalsResponse)
def get_festivals(year: int, city_id: str | None = None, lat: float | None = None, lng: float | None = None):
    """Returns major festivals for the year with computed local dates."""
    if city_id is None and (lat is None or lng is None):
        raise HTTPException(status_code=400, detail="Provide city_id or both lat and lng")
    return panchang.compute_festivals(year=year, city_id=city_id, lat=lat, lng=lng)


@app.get("/api/calendar/highlights", response_model=CalendarHighlightsResponse)
def get_calendar_highlights(month: str, city_id: str | None = None, lat: float | None = None, lng: float | None = None):
    """Returns month-spanning highlights used by the homepage calendar frame."""
    if city_id is None and (lat is None or lng is None):
        raise HTTPException(status_code=400, detail="Provide city_id or both lat and lng")
    return panchang.compute_monthly_highlights(month=month, city_id=city_id, lat=lat, lng=lng)


@app.get("/api/calendar/location-context", response_model=ResolvedLocationResponse)
def get_location_context(lat: float, lng: float):
    """Resolves a requested lat/lng to the closest supported city for editorial calendar fallbacks."""
    return panchang.resolve_location(lat=lat, lng=lng)


@app.post("/api/calendar/ritual-muhurta")
def get_ritual_muhurta(city_id: str, date_from: str, date_to: str, ritual_type: str):
    """Segmented-day muhurta recommendation for a ritual type over a date range."""
    return panchang.compute_ritual_windows(
        city_id=city_id, date_from=date_from, date_to=date_to, ritual_type=ritual_type
    )
