"""Minimal city lookup for the calendar service.

MVP: hardcoded seed data for major German cities. Once the events_service
database is the single source of truth for city taxonomy, this should be
replaced with a call to that service (or a shared cities table) instead of
duplicating city data across services.
"""

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
