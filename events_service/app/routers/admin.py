"""Admin moderation API: pending submissions, approve/reject, taxonomy CRUD."""
from fastapi import APIRouter, Depends

router = APIRouter()


@router.get("/submissions")
def list_pending_submissions(city_id: str = None, status: str = None):
    """Filterable list of submitted/under_review events for moderation."""
    raise NotImplementedError("Requires admin role check + filters.")


@router.post("/submissions/{event_id}/approve")
def approve_event(event_id: str, admin_user=Depends(lambda: None)):
    """Approve event, log reviewed_by_admin_id + timestamp for audit trail."""
    raise NotImplementedError("Set status=approved, reviewed_by_admin_id, audit log entry.")


@router.post("/submissions/{event_id}/reject")
def reject_event(event_id: str, reason: str, admin_user=Depends(lambda: None)):
    """Reject event; rejection reason is mandatory and stored in review_notes."""
    raise NotImplementedError("Set status=rejected, review_notes=reason, audit log entry.")


@router.get("/cities")
def list_cities():
    raise NotImplementedError("CRUD for city taxonomy.")


@router.get("/categories")
def list_categories():
    raise NotImplementedError("CRUD for event category taxonomy.")
