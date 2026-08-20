"""Curated festival ruleset — seed data for pan-Indian festivals.

Astronomy alone is not sufficient for festival dates; scriptural rules
determine specific windows (e.g. Lakshmi Puja in Pradosh Kaal after sunset
on Diwali). This module stores rule hints; compute_festivals() in
panchang.py applies them against computed tithi/nakshatra data.
"""

FESTIVALS = [
    {
        "id": "diwali",
        "name": "Diwali (Lakshmi Puja)",
        "type": "main_festival",
        "rule_hint": "Amavasya in Kartik month; puja window in Pradosh Kaal after sunset.",
    },
    {
        "id": "navratri",
        "name": "Navratri",
        "type": "main_festival",
        "rule_hint": "Nine nights starting Shukla Paksha Pratipada in Ashwin month.",
    },
    {
        "id": "ganesh_chaturthi",
        "name": "Ganesh Chaturthi",
        "type": "main_festival",
        "rule_hint": "Shukla Paksha Chaturthi in Bhadrapada month.",
    },
    {
        "id": "holi",
        "name": "Holi",
        "type": "main_festival",
        "rule_hint": "Purnima in Phalguna month.",
    },
    {
        "id": "ram_navami",
        "name": "Ram Navami",
        "type": "main_festival",
        "rule_hint": "Shukla Paksha Navami in Chaitra month.",
    },
    {
        "id": "ekadashi",
        "name": "Ekadashi (fasting day)",
        "type": "fasting",
        "rule_hint": "Recurs twice per lunar month (Shukla and Krishna Paksha, 11th tithi).",
    },
    {
        "id": "purnima",
        "name": "Purnima (full moon)",
        "type": "fasting",
        "rule_hint": "Full moon tithi, once per lunar month.",
    },
]
