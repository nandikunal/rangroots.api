"""Public events API: list, filter, search, submit, edit own submissions."""
from fastapi import APIRouter, Depends, Query
from typing import Optional

router = APIRouter()


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
    raise NotImplementedError("Wire up DB query with filters + pagination.")


@router.get("/{event_id}")
def get_event(event_id: str):
    """Single event detail. Visitor-accessible."""
    raise NotImplementedError("Fetch event by id.")


@router.post("", status_code=201)
def create_event(payload: dict, current_user=Depends(lambda: None)):
    """Creates a new event in `submitted` status. Requires authentication."""
    raise NotImplementedError("Requires auth dependency + status=submitted on create.")


@router.patch("/{event_id}")
def update_event(event_id: str, payload: dict, current_user=Depends(lambda: None)):
    """Owner (pre-approval) or admin can edit. Permission-checked at row level."""
    raise NotImplementedError("Check ownership or admin role before allowing edit.")
