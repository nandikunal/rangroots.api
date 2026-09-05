"""Minimal city lookup for the calendar service.

MVP: hardcoded seed data for major German cities. Once the events_service
database is the single source of truth for city taxonomy, this should be
replaced with a call to that service (or a shared cities table) instead of
duplicating city data across services.
"""

from math import asin, cos, radians, sin, sqrt

CITIES = {
    "berlin": {"name": "Berlin", "country": "Germany", "timezone": "Europe/Berlin", "latitude": 52.5200, "longitude": 13.4050},
    "munich": {"name": "Munich", "country": "Germany", "timezone": "Europe/Berlin", "latitude": 48.1351, "longitude": 11.5820},
    "hamburg": {"name": "Hamburg", "country": "Germany", "timezone": "Europe/Berlin", "latitude": 53.5511, "longitude": 9.9937},
    "frankfurt": {"name": "Frankfurt", "country": "Germany", "timezone": "Europe/Berlin", "latitude": 50.1109, "longitude": 8.6821},
    "cologne": {"name": "Cologne", "country": "Germany", "timezone": "Europe/Berlin", "latitude": 50.9375, "longitude": 6.9603},
    "stuttgart": {"name": "Stuttgart", "country": "Germany", "timezone": "Europe/Berlin", "latitude": 48.7758, "longitude": 9.1829},
}


def get_city(city_id: str) -> dict:
    city = CITIES.get(city_id.lower())
    if city is None:
        raise ValueError(
            f"Unknown city_id '{city_id}'. Supported cities: {', '.join(CITIES.keys())}"
        )
    return city


def _haversine_km(lat_a: float, lng_a: float, lat_b: float, lng_b: float) -> float:
    earth_radius_km = 6371.0
    lat_delta = radians(lat_b - lat_a)
    lng_delta = radians(lng_b - lng_a)
    start = radians(lat_a)
    end = radians(lat_b)

    haversine = sin(lat_delta / 2) ** 2 + cos(start) * cos(end) * sin(lng_delta / 2) ** 2
    return 2 * earth_radius_km * asin(sqrt(haversine))


def resolve_nearest_city(lat: float, lng: float) -> tuple[str, dict, float]:
    nearest_city_id = ""
    nearest_city = None
    nearest_distance_km = float("inf")

    for city_id, city in CITIES.items():
        distance_km = _haversine_km(lat, lng, city["latitude"], city["longitude"])
        if distance_km < nearest_distance_km:
            nearest_city_id = city_id
            nearest_city = city
            nearest_distance_km = distance_km

    if nearest_city is None:
        raise ValueError("No configured cities are available for location resolution")

    return nearest_city_id, nearest_city, round(nearest_distance_km, 1)
