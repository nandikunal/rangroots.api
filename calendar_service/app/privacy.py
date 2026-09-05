"""Privacy helper definitions for location and data consent flow.

This is intentionally lightweight and declarative. The application enforces privacy
consent at the frontend and stores only user-approved preferences locally. The API
layer remains location-aware but does not require persistent user tracking.
"""

PRIVACY_NOTICE = {
    "title": "Location privacy",
    "summary": "We request precise location only to calculate local Panchang for your current place.",
    "storage": "Coordinates are kept in browser memory or user-approved local storage only when you choose to save location preferences.",
    "sharing": "We do not sell or share exact coordinates with third parties.",
    "revocation": "You can revoke permission anytime via browser permissions or the app settings panel.",
}
