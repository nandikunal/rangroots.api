"""Public events API: list, filter, search, submit, edit own submissions."""
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

router = APIRouter()


EVENTS = [
    {
        "id": "evt-krishna-janmashtami-berlin-2026",
        "city_id": "berlin",
        "title": "Krishna Janmashtami Celebration",
        "description": "Temple bhajans, midnight aarti, and youth performances for Janmashtami.",
        "start_datetime": "2026-09-03T17:30:00+02:00",
        "end_datetime": "2026-09-04T00:30:00+02:00",
        "venue_name": "Berlin Hindu Mandir",
        "event_category": "festival",
        "is_free": True,
    },
    {
        "id": "evt-paryushana-frankfurt-2026",
        "city_id": "frankfurt",
        "title": "Paryushana Pravachan Series",
        "description": "Daily discourse, pratikraman, and family observance guidance during Paryushana.",
        "start_datetime": "2026-09-08T18:00:00+02:00",
        "end_datetime": "2026-09-08T20:30:00+02:00",
        "venue_name": "Jain Center Frankfurt",
        "event_category": "community",
        "is_free": True,
    },
    {
        "id": "evt-ganesh-munich-2026",
        "city_id": "munich",
        "title": "Ganesh Chaturthi Sthapana",
        "description": "Murti sthapana, cultural program, and prasadam seva for Ganesh Chaturthi.",
        "start_datetime": "2026-09-14T10:00:00+02:00",
        "end_datetime": "2026-09-14T14:30:00+02:00",
        "venue_name": "Munich Cultural Hall",
        "event_category": "festival",
        "is_free": False,
    },
    {
        "id": "evt-pitru-hamburg-2026",
        "city_id": "hamburg",
        "title": "Pitru Paksha Remembrance Sabha",
        "description": "Guided remembrance observance with priest consultation for Pitru Paksha.",
        "start_datetime": "2026-09-27T09:00:00+02:00",
        "end_datetime": "2026-09-27T11:00:00+02:00",
        "venue_name": "Hamburg Dharma Center",
        "event_category": "community",
        "is_free": True,
    },
    {
        "id": "evt-gandhi-cologne-2026",
        "city_id": "cologne",
        "title": "Gandhi Jayanti Community Gathering",
        "description": "Intergenerational reflection, readings, and seva sign-ups honoring Gandhi Jayanti.",
        "start_datetime": "2026-10-02T18:30:00+02:00",
        "end_datetime": "2026-10-02T20:00:00+02:00",
        "venue_name": "Cologne Indian Association",
        "event_category": "community",
        "is_free": True,
    },
    {
        "id": "evt-navaratri-berlin-2026",
        "city_id": "berlin",
        "title": "Navaratri Garba Night",
        "description": "Community dance, live music, and food stalls during Navaratri weekend.",
        "start_datetime": "2026-10-17T19:00:00+02:00",
        "end_datetime": "2026-10-17T23:30:00+02:00",
        "venue_name": "Berlin Community Arena",
        "event_category": "social_cultural",
        "is_free": False,
    },
]


def _parse_iso(value: str) -> datetime:
    return datetime.fromisoformat(value)


def _normalize_optional_text(value: object) -> Optional[str]:
    return value if isinstance(value, str) and value else None


def _matches_query(event: dict, query: str) -> bool:
    haystack = " ".join(
        [
            event.get("title", ""),
            event.get("description", ""),
            event.get("venue_name", ""),
            event.get("event_category", ""),
        ]
    ).lower()
    return query.lower() in haystack


def _in_date_range(event: dict, date_from: Optional[str], date_to: Optional[str]) -> bool:
    start = _parse_iso(event["start_datetime"])
    date_from = _normalize_optional_text(date_from)
    date_to = _normalize_optional_text(date_to)
    if date_from:
        from_dt = datetime.fromisoformat(f"{date_from}T00:00:00+00:00")
        if start < from_dt:
            return False
    if date_to:
        to_dt = datetime.fromisoformat(f"{date_to}T23:59:59+00:00")
        if start > to_dt:
            return False
    return True


@router.get("")
def list_events(
    city_id: Optional[str] = None,
    date_from: Optional[str] = Query(None, alias="from"),
    date_to: Optional[str] = Query(None, alias="to"),
    category: Optional[str] = None,
    is_free: Optional[bool] = None,
    state_tag: Optional[str] = None,
    q: Optional[str] = None,
):
    """Paginated list of events matching filters. Visitor-accessible."""
    city_id = _normalize_optional_text(city_id)
    category = _normalize_optional_text(category)
    q = _normalize_optional_text(q)
    filtered = []
    for event in EVENTS:
        if city_id and event["city_id"] != city_id:
            continue
        if category and event["event_category"] != category:
            continue
        if is_free is not None and event["is_free"] != is_free:
            continue
        if q and not _matches_query(event, q):
            continue
        if not _in_date_range(event, date_from, date_to):
            continue
        filtered.append(event)

    filtered.sort(key=lambda event: event["start_datetime"])
    return filtered


@router.get("/{event_id}")
def get_event(event_id: str):
    """Single event detail. Visitor-accessible."""
    for event in EVENTS:
        if event["id"] == event_id:
            return event
    raise HTTPException(status_code=404, detail="Event not found")


@router.post("", status_code=201)
def create_event(payload: dict, current_user=Depends(lambda: None)):
    """Creates a new event in `submitted` status. Requires authentication."""
    raise NotImplementedError("Requires auth dependency + status=submitted on create.")


@router.patch("/{event_id}")
def update_event(event_id: str, payload: dict, current_user=Depends(lambda: None)):
    """Owner (pre-approval) or admin can edit. Permission-checked at row level."""
    raise NotImplementedError("Check ownership or admin role before allowing edit.")
