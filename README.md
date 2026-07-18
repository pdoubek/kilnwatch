# KilnWatch

Thermocouple monitoring, data logging, and firing program visualization for glass and
ceramic kilns. Runs on a Raspberry Pi 4; serves a web interface for remote monitoring
from home or a mobile device.

**Current phase:** Monitor & Log (read-only — no kiln control yet)
**Target kiln:** Skutt 818 ceramic kiln
**Thermocouples:** Up to 4 K-type via MAX31856 amplifier boards on SPI

---

## Quick Start (Development — No Hardware Required)

```bash
git clone https://github.com/YOUR_USERNAME/kilnwatch.git
cd kilnwatch
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env              # edit: set WEB_USERNAME and WEB_PASSWORD_HASH
cp config/settings.example.toml config/settings.toml   # edit as needed

python scripts/init_db.py         # create the database schema
python scripts/simulate_tc.py &   # fake thermocouple readings
python -m kilnwatch.main          # start the app
```

Open `http://localhost:5000` in a browser.

---

## Deployment (Raspberry Pi)

See `deploy/README.md` for:
- Pi OS setup and SPI enable
- Wiring the MAX31856 boards
- systemd service installation
- Remote access configuration (Cloudflare Tunnel or DDNS)
- Chromium kiosk mode for the touchscreen

---

## Project Documentation

Design decisions, hardware specs, and architectural guidelines are in `.kiro/steering/`:

| File | Contents |
|---|---|
| `product.md` | Goals, requirements, phases, what's out of scope |
| `tech.md` | Hardware choices, software stack, GPIO map, decisions log |
| `structure.md` | Directory layout, module boundaries, conventions |

---

## License

[TBD]
