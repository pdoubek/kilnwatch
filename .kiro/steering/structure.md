# KilnWatch — Project Structure

## Directory Layout

```
Kilnwatch/
├── .kiro/
│   └── steering/
│       ├── product.md          # Goals, requirements, phases, operator context
│       ├── tech.md             # Hardware/software stack, GPIO map, decisions log
│       └── structure.md        # This file — layout, conventions, open questions
│
├── config/
│   ├── settings.toml           # Active config (version-controlled; no secrets)
│   └── settings.example.toml  # Template with all keys and defaults
│
├── data/                       # GITIGNORED — SQLite DB and CSV exports
│   └── kilnwatch.db
│
├── logs/                       # GITIGNORED — runtime logs
│
├── kilnwatch/                  # Main Python package
│   ├── __init__.py
│   ├── main.py                 # Entry point: starts scheduler + web server
│   │
│   ├── hardware/               # Hardware interface — only place that touches SPI/GPIO
│   │   ├── __init__.py
│   │   ├── thermocouple.py     # MAX31856 read logic, CS pin management
│   │   └── gpio_config.py      # Pin assignments, SPI bus setup
│   │
│   ├── data/                   # Data layer — only place that touches SQLAlchemy
│   │   ├── __init__.py
│   │   ├── models.py           # ORM models: Session, Reading, Thermocouple, Program, Segment
│   │   ├── database.py         # Engine init, session factory
│   │   └── repository.py       # All CRUD — routes call these, not SQLAlchemy directly
│   │
│   ├── scheduler/              # Background sampling — runs independently of web server
│   │   ├── __init__.py
│   │   └── sampler.py          # APScheduler job: read TCs → write readings to DB
│   │
│   ├── web/                    # Flask application
│   │   ├── __init__.py
│   │   ├── app.py              # App factory, SocketIO init, blueprint registration
│   │   ├── auth.py             # Login/logout routes, session guard decorator
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── dashboard.py    # Live view: current temps, active session status
│   │   │   ├── history.py      # Past sessions: list, graph, export
│   │   │   ├── programs.py     # Firing program CRUD (create, edit, delete, activate)
│   │   │   └── config.py       # TC labeling, enable/disable, sample interval
│   │   ├── templates/
│   │   │   ├── base.html       # Layout, nav, SocketIO client script
│   │   │   ├── dashboard.html
│   │   │   ├── history.html
│   │   │   ├── programs.html
│   │   │   └── config.html
│   │   └── static/
│   │       ├── css/
│   │       └── js/
│   │
│   └── utils/
│       ├── __init__.py
│       ├── config.py           # Loads settings.toml + .env; exposes typed config object
│       └── logging_setup.py    # Configures root logger from settings
│
├── tests/
│   ├── __init__.py
│   ├── test_thermocouple.py    # Hardware tests using mocked SPI
│   ├── test_repository.py      # DB layer tests against in-memory SQLite
│   └── test_routes.py          # Web route tests via Flask test client
│
├── scripts/
│   ├── init_db.py              # One-time: create DB schema
│   ├── export_session.py       # Export a firing session to CSV
│   └── simulate_tc.py          # Fake TC readings for dev without hardware
│
├── deploy/
│   ├── kilnwatch.service       # systemd unit file
│   └── README.md               # Pi setup, service install, remote access, kiosk mode
│
├── .env                        # GITIGNORED — secrets (web credentials)
├── .env.example                # Committed template — key names only, no values
├── .gitignore
├── README.md                   # Project overview, quick start
├── requirements.txt            # Pinned production deps
├── requirements-dev.txt        # Dev/test deps (pytest, etc.)
└── pyproject.toml              # Project metadata, tool config (black, ruff, pytest)
```

---

## Architectural Boundaries

These separations are intentional and should be maintained:

| Layer | Module | Rule |
|---|---|---|
| Hardware | `kilnwatch/hardware/` | Only module that imports spidev, RPi.GPIO, or adafruit libs |
| Data | `kilnwatch/data/` | Only module that imports SQLAlchemy or touches the DB file |
| Scheduling | `kilnwatch/scheduler/` | Calls hardware layer to read, calls data layer to write |
| Web | `kilnwatch/web/` | Calls data layer (repository) only; never touches hardware directly |
| Config | `kilnwatch/utils/config.py` | Loaded once at startup; passed as needed — not re-read per function |

This structure means the hardware layer can be mocked for testing and development on a
non-Pi machine, and the web layer can be tested without real TC hardware.

---

## Conventions

### Python
- Type hints on all function signatures
- Docstrings on all public functions and classes
- No bare `except:` — always catch specific exceptions
- Logging via `logging` module; no `print()` in production code

### Git
- Commit messages: imperative present tense ("Add TC label support")
- `main` = deployable/stable; `dev` = active work
- Merge `dev` → `main` when stable; tag on Pi deployment (`v0.1.0`, etc.)
- Never commit: `.env`, `data/`, `logs/`, `venv/`

### Configuration
- Non-secret settings in `config/settings.toml` (version-controlled)
- Secrets (credentials) in `.env` only (gitignored)
- `settings.example.toml` and `.env.example` always kept current with new keys

---

## Open Questions

- [ ] Remote access: Cloudflare Tunnel vs. DDNS + port-forward
- [ ] On-device UI: Chromium kiosk (reuse web UI) vs. Python GUI (Tkinter/PyQt6)
- [ ] Display: DSI 7" touchscreen vs. HDMI
- [ ] Units: °F default (matches Skutt controller) — make configurable
- [ ] SD card write strategy: WAL mode for SQLite; periodic VACUUM to limit wear
- [ ] Whether `simulate_tc.py` should emulate a real ramp profile or just random temps
