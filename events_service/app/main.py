"""FastAPI entrypoint for the Events service.

City-wise Indian community events discovery, submission workflow, and admin
moderation. Independently deployable from the calendar service.
"""
from fastapi import FastAPI
from app.routers import events, admin, auth

app = FastAPI(title="Rang Roots Events Service", version="0.1.0")

app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
