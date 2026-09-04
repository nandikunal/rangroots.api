"""Pydantic response/request schemas for the calendar service."""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class DailyPanchangResponse(BaseModel):
    date: str
    city_id: str
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
    category: str = "other"
    type: Optional[str] = None
    rule_hint: Optional[str] = None
    description: Optional[str] = None
    year: Optional[int] = None


class FestivalsResponse(BaseModel):
    year: int
    city_id: str
    festivals: List[FestivalEntry] = []
