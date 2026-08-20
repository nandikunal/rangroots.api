"""Pydantic response/request schemas for the calendar service."""
from pydantic import BaseModel
from typing import List, Dict, Any


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
