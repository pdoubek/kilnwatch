# KilnWatch — Technical Stack

## Hardware

### Host Platform
- **Device:** Raspberry Pi 4 (2GB RAM minimum; 4GB preferred)
- **OS:** Raspberry Pi OS (64-bit, Lite or Desktop — TBD based on display approach)
- **Storage:** 32–64GB microSD card (Class 10 / A1 or better)
- **Power:** Official Raspberry Pi 4 USB-C power supply (5.1V/3A)

### Display
- **Primary candidate:** Raspberry Pi 7" Official Touchscreen (DSI connection)
  - Resolution: 800×480, 10-point capacitive touch
- **Alternative:** HDMI monitor (headless + web-only UI)
- **Decision:** PENDING — update when confirmed

### Thermocouple Amplifiers
- **Chip:** MAX31856 (universal TC type, 19-bit resolution, SPI)
- **Boards:** No-name/clone breakout boards (Adafruit form-factor)
  - Known issue: clones may omit bypass caps per Maxim datasheet
  - Mitigation: add 100nF across TC+/TC- and 10nF across VCC/GND if noise observed
- **Quantity:** 1–4 boards on shared SPI bus; one CS GPIO per board
- **Interface:** Hardware SPI via Pi GPIO header

### Thermocouple Sensors
- **Type:** K-type (operator-owned)
- **Max temp:** ~1350°C rated; kiln max ~1100°C (cone 6)

### GPIO Pin Allocation (SPI + CS lines)
```
SPI0 MOSI  — GPIO 10 (pin 19)
SPI0 MISO  — GPIO 9  (pin 21)
SPI0 SCLK  — GPIO 11 (pin 23)
CS0 (TC1)  — GPIO 8  (pin 24)  [SPI0_CE0 — hardware CS]
CS1 (TC2)  — GPIO 7  (pin 26)  [SPI0_CE1 — hardware CS]
CS2 (TC3)  — GPIO 25 (pin 22)  [software CS]
CS3 (TC4)  — GPIO 24 (pin 18)  [software CS]
```
NOTE: Verify these assignments against actual wiring before finalizing.

### Networking
- **Primary:** Pi 4 onboard WiFi (802.11ac)
- **Fallback:** Pi 4 onboard Gigabit Ethernet
- **Remote access:** PENDING — Cloudflare Tunnel (preferred, no port-forward needed)
  or DDNS + router port-forward

---

## Software Stack

### OS & Runtime
- Raspberry Pi OS Bookworm (64-bit)
- Python 3.11+
- Virtual environment: `venv` at project root (gitignored)

### Python Dependencies
| Package | Purpose |
|---|---|
| `adafruit-circuitpython-max31856` | MAX31856 SPI driver (works on Pi via blinka) |
| `adafruit-blinka` | CircuitPython compatibility layer for Pi |
| `RPi.GPIO` | GPIO control for software CS lines |
| `spidev` | Low-level SPI access |
| `flask` | Web server |
| `flask-socketio` | WebSocket for real-time graph push |
| `sqlalchemy` | ORM / DB abstraction |
| `plotly` | Graph data (served as JSON to Plotly.js in browser) |
| `apscheduler` | Background TC sampling scheduler |
| `pydantic` | Config and data validation |
| `python-dotenv` | .env secret loading |
| `tomllib` | TOML config parsing (stdlib in Python 3.11+) |

### Database
- **Engine:** SQLite via SQLAlchemy
- **File:** `data/kilnwatch.db` (gitignored)
- **Tables:**
  - `sessions` — firing session records (id, name, start_time, end_time, notes)
  - `readings` — TC readings (id, session_id, tc_id, timestamp, temp_c)
  - `thermocouples` — TC config (id, label, enabled, cs_pin)
  - `programs` — named firing programs (id, name, notes, created_at)
  - `segments` — program steps (id, program_id, order_index, ramp_rate_per_hour, setpoint, hold_minutes)

### Web Framework
- Flask + Flask-SocketIO
- Jinja2 templates (server-rendered HTML)
- Plotly.js for in-browser graph rendering (data fetched as JSON)
- Session-based auth (credentials in .env, never in config file)

### On-Device UI
- **Candidate A:** Chromium browser in kiosk mode pointing at localhost:5000
  - Reuses web UI; no separate codebase; requires Pi OS Desktop or a compositor
- **Candidate B:** Python GUI (Tkinter or PyQt6)
  - More control over touch UX; separate codebase to maintain
- **Decision:** PENDING — test Chromium kiosk first; fall back to Python GUI if touch
  experience is inadequate

### Configuration Files
- `config/settings.toml` — non-secret config (TC pins, labels, intervals, web port)
- `.env` — secrets only (web credentials)
- `config/settings.example.toml` + `.env.example` are version-controlled templates

---

## Decisions Log

| Date | Decision | Rationale |
|---|---|---|
| 2025-07 | Raspberry Pi 4 over ESP32 | HDMI/DSI display, full Python, web server, future control headroom |
| 2025-07 | MAX31856 over MAX31855 | Multi-type TC, better resolution, better cold-junction compensation |
| 2025-07 | Flask over FastAPI | Adequate for single-user embedded; simpler; more community examples |
| 2025-07 | SQLite over flat CSV | Session management, program/reading joins, query flexibility |
| PENDING | Remote access method | Cloudflare Tunnel vs. DDNS+port-forward |
| PENDING | On-device GUI method | Chromium kiosk vs. Python GUI |
| PENDING | Display connection | DSI (7" official touchscreen) vs. HDMI |

---

## Development Machine
- **OS:** [FILL IN]
- **Editor:** [FILL IN]
- **Python:** [FILL IN version]
- **Git remote:** https://github.com/[YOUR_USERNAME]/kilnwatch (private repo)
