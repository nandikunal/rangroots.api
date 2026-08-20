# rangroots.api

Backend services for **Rang Roots** — a Hindu calendar/muhurta and Indian community events portal for Indians in Europe (starting with Germany).

## Architecture

Two decoupled, independently deployable services behind a single API gateway:

- **`calendar_service/`** — stateless panchang & muhurta engine (tithi, nakshatra, yoga, karana, sunrise/sunset, festivals, ritual planner).
- **`events_service/`** — city-wise Indian community events discovery, submission workflow, and admin moderation.

## Key architectural decision: ephemeris engine

We use **[Astronomy Engine](https://github.com/cosinekitty/astronomy)** (MIT license) as the underlying planetary position engine, **not** Swiss Ephemeris / `pyswisseph`.

Swiss Ephemeris is dual-licensed AGPL-3.0 OR a paid commercial license. Since AGPL-3.0 §13 requires any networked service built on it to release its *entire* source code to users, it is not viable for a closed-source SaaS without purchasing the commercial license. Astronomy Engine (MIT) provides adequate accuracy (±1 arcminute, VSOP87-class) for panchang-grade calculations with zero licensing obligations.

See `docs/build-vs-buy.md` for the full evaluation.

## Stack

- Python 3.11+, FastAPI
- PostgreSQL (structured data), Redis (caching)
- JWT-based auth, RBAC (Visitor / Registered User / Admin, City Moderator planned)
- Deployed on Azure Kubernetes Service

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Repository layout

```
rangroots.api/
├── calendar_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── panchang.py       # tithi/nakshatra/yoga/karana derivation
│   │   ├── ephemeris.py      # thin wrapper around astronomy-engine
│   │   ├── festivals.py      # curated festival ruleset
│   │   └── schemas.py
│   └── requirements.txt
├── events_service/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py         # Event, City, User, Category, Tag
│   │   ├── routers/
│   │   │   ├── events.py
│   │   │   ├── admin.py
│   │   │   └── auth.py
│   │   └── schemas.py
│   └── requirements.txt
├── docs/
│   ├── build-vs-buy.md
│   └── data-model.md
└── README.md
```

## License

TBD — to be decided before public release. Internal development for now.
