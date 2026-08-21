"""JWT-based authentication for registered users and admins."""
from fastapi import APIRouter

router = APIRouter()


@router.post("/register")
def register(payload: dict):
    raise NotImplementedError("Create user with role=registered, hash password.")


@router.post("/login")
def login(payload: dict):
    raise NotImplementedError("Verify credentials, issue JWT access/refresh tokens.")
