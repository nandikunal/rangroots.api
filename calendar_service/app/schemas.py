"""Pydantic response/request schemas for the calendar service."""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class LocationContext(BaseModel):
    requested_latitude: Optional[float] = None
    requested_longitude: Optional[float] = None
    resolved_city_id: str
    resolved_city_name: str
    timezone: str
    distance_km: float


class DailyPanchangResponse(BaseModel):
    date: str
    city_id: str
    location_context: Optional[LocationContext] = None
    tithi: str
    paksha: str
    nakshatra: str
    yoga: str
    karana: str
    sunrise: str
    sunset: str
    festivals: List[str] = []
    muhurtas: Dict[str, Any] = {}


class FestivalEntry(BaseModel):
    """A single entry in the /api/calendar/festivals response.

    category is the display taxonomy used by front-end clients to group
    festivals into sections (festival | deity | observance | other).
    type/rule_hint/fixed_date/id are retained from the curated ruleset
    in festivals.py for backward compatibility.
    """
    id: str
    name: str
    date: str
    end_date: Optional[str] = None
    category: str = "other"
    type: Optional[str] = None
    rule_hint: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None


class FestivalsResponse(BaseModel):
    year: int
    city_id: str
    location_context: Optional[LocationContext] = None
    festivals: List[FestivalEntry] = []


class CalendarHighlight(BaseModel):
    id: str
    name: str
    start_date: str
    end_date: str
    category: str = "other"


class CalendarHighlightsResponse(BaseModel):
    month: str
    city_id: str
    location_context: Optional[LocationContext] = None
    highlights: List[CalendarHighlight] = []


class MonthlyPanchangResponse(BaseModel):
    month: str
    city_id: str
    location_context: Optional[LocationContext] = None
    days: List[DailyPanchangResponse] = []


class ResolvedLocationResponse(LocationContext):
    requested_latitude: float
    requested_longitude: float
