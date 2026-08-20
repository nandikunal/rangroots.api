# Build vs Buy — Astronomical Engine & Events Platform

## Ephemeris engine

| Option | License | Verdict |
|---|---|---|
| Swiss Ephemeris / pyswisseph | AGPL-3.0 OR paid commercial (CHF 700 / 99yr) | Rejected for default path — AGPL forces full source disclosure for networked services |
| **Astronomy Engine (cosinekitty/astronomy)** | **MIT** | **Selected** — adequate accuracy (±1 arcminute), multi-language, no obligations |
| XALEN Ephemeris (vedika-io/xalen-ephemeris) | Apache-2.0 | Backup option — newer, pure-Rust, optional JPL DE440 precision |

Panchang derivation (tithi, nakshatra, yoga, karana, Lahiri ayanamsa, sunrise/sunset with refraction) is implemented in-house on top of Astronomy Engine's raw planetary positions — this layer is standard, well-documented Vedic astronomy math and is not available pre-packaged under a permissive license.

## Events platform

Evaluated Attendize (4.2k★) and Hi.Events (4.0k★) — both are full ticketing platforms in Laravel/PHP under non-standard "Other" licenses, and both are scoped for ticket sales rather than lightweight discovery + moderation. Building the events service from scratch in FastAPI was confirmed as the correct choice: the core logic (status workflow, city taxonomy, moderation audit trail) is product-specific and not a solved infrastructure problem.
