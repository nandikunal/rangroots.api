"""Curated festival ruleset — seed data for pan-Indian festivals.

Astronomy alone is not sufficient for festival dates; scriptural rules
determine specific windows (e.g. Lakshmi Puja in Pradosh Kaal after sunset
on Diwali). This module stores rule hints plus fixed_date values for the
current seed year (2026) so compute_daily() has something concrete to match
against.

Each entry also carries a "category" field — one of "festival", "deity",
"observance", "other" — used by the front-end to group festivals into
sections (see rangroots.app /calendar page). This is a display taxonomy,
distinct from "type" (which currently only distinguishes "main_festival";
kept for backward compatibility and possible future sub-typing).

TODO (follow-up): compute fixed_date per-year from tithi/nakshatra rules
instead of hardcoding, so this works for any year without manual updates.
Current hardcoded dates are for calendar year 2026 (India Standard Time
dates; not yet adjusted per-city per docs/build-vs-buy.md hybrid model).
"""

FESTIVALS = [
    {
        "id": "diwali",
        "name": "Diwali (Lakshmi Puja)",
        "type": "main_festival",
        "category": "festival",
        "rule_hint": "Amavasya in Kartik month; puja window in Pradosh Kaal after sunset.",
        "fixed_date": "2026-11-08",
    },
    {
        "id": "navratri",
        "name": "Navratri (starts)",
        "type": "main_festival",
        "category": "deity",
        "rule_hint": "Nine nights starting Shukla Paksha Pratipada in Ashwin month.",
        "fixed_date": "2026-10-11",
    },
    {
        "id": "ganesh_chaturthi",
        "name": "Ganesh Chaturthi",
        "type": "main_festival",
        "category": "deity",
        "rule_hint": "Shukla Paksha Chaturthi in Bhadrapada month.",
        "fixed_date": "2026-09-14",
    },
    {
        "id": "holi",
        "name": "Holi",
        "type": "main_festival",
        "category": "festival",
        "rule_hint": "Purnima in Phalguna month.",
        "fixed_date": "2026-03-04",
    },
    {
        "id": "ram_navami",
        "name": "Ram Navami",
        "type": "main_festival",
        "category": "deity",
        "rule_hint": "Shukla Paksha Navami in Chaitra month.",
        "fixed_date": "2026-03-27",
    },
]
