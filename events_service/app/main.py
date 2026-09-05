"""FastAPI entrypoint for the Events service.

City-wise Indian community events discovery, submission workflow, and admin
moderation. Independently deployable from the calendar service.
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import events, admin, auth

app = FastAPI(title="Rang Roots Events Service", version="0.1.0")

allowed_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")
app.add_middleware(
	CORSMiddleware,
	allow_origins=[origin.strip() for origin in allowed_origins if origin.strip()],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(events.router, prefix="/api/events", tags=["events"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
