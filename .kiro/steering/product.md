# KilnWatch — Product Overview

## Purpose
KilnWatch is a thermocouple monitoring and data logging system for glass and ceramic kilns.
It reads up to 4 thermocouples, stores time-series data, displays real-time graphs, and serves
a web interface for remote monitoring and configuration. The eventual goal is to evolve into a
full programmable multi-zone kiln controller.

## Background
The kiln currently in use is a Skutt 818 ceramic kiln with its proprietary controller. For now,
KilnWatch is read-only — it observes and records. Firing programs are entered independently on
the Skutt controller AND into KilnWatch (for overlay display on graphs). Control capability will
be added in a future phase.

The shop is not co-located with the operator's home or workplace. Remote monitoring — including
the ability to check status, adjust configurations, and terminate a firing — is a primary
requirement, not a nice-to-have.

## Core Requirements (Phase 1 — Monitor & Log)

### Thermocouple Input
- Read 1–4 K-type thermocouples simultaneously
- Each thermocouple is user-labeled (e.g., "Top Zone", "Bottom Zone", "Shelf 1")
- Labels appear in stored data and on graphs
- Hardware: MAX31856 breakout boards (no-name/clone), one per thermocouple, on shared SPI bus

### Data Logging
- Log all thermocouple readings with timestamps to persistent storage
- Configurable sample interval (default: 30 seconds; range: 5s–5min)
- Storage on local SD card; offload/backup to networked computer supported
- SQLite database preferred for query flexibility

### Display
- On-device display: Raspberry Pi 7" official touchscreen (HDMI/DSI)
- Real-time time-series graph of all active thermocouples
- Firing program overlay on graph (ramp/hold segments as stepped lines)
- On-device touch UI for viewing data and entering/editing firing programs

### Web Interface
- Hosted on the device (Flask or FastAPI)
- Accessible from home/work over the internet (not just LAN)
- Real-time or near-real-time graph display (auto-refreshing or WebSocket)
- Remote ability to: view current temps, view/edit firing program, start/stop logging session
- Authentication required (this device is internet-accessible)

### Firing Program Entry
- A firing program consists of 4–6 segments
- Each segment defines: ramp rate (°F or °C per hour), target setpoint, hold time
- Typical structure: heat → hold → heat → hold → cool → hold
- Program is stored in the database and overlaid on the temperature graph as a reference curve
- Programs are named and saved for reuse

### Networking
- Primary: WiFi (WPA2, connects to existing shop network)
- Optional: wired Ethernet fallback
- Remote access: either via port forwarding + DDNS, or a tunneling service (e.g., Cloudflare Tunnel, ngrok)
- Authentication on web interface mandatory before remote access is enabled

## Future Phase — Kiln Control
- Drive solid-state relays (SSR) to control heating elements
- PID or ramp-and-soak control loop per zone
- Emergency shutoff logic (overtemp, sensor fault, runaway detection)
- All firing programming done on KilnWatch; Skutt controller bypassed

## Non-Goals (Phase 1)
- No control of heating elements
- No integration with Skutt proprietary protocol
- No cloud data storage (local only in Phase 1)
- No multi-kiln support (single Skutt 818)

## Operator Context
- Operator: experienced systems/network engineer, moderate Python, moderate electronics background
- Primary interface: web browser from home or mobile device while away from shop
- Secondary interface: touchscreen on device at the kiln
- Prefers direct technical responses; can ask follow-up questions on unfamiliar details

## Open Items — UPDATE THIS SECTION AS VISION EVOLVES
- [ ] Confirm remote access method (Cloudflare Tunnel vs. DDNS + port-forward)
- [ ] Confirm display choice (7" DSI touchscreen vs. HDMI)
- [ ] Confirm on-device UI approach (Chromium kiosk vs. Python GUI)
- [ ] Define units default (°F vs. °C — likely °F to match Skutt controller)
- [ ] Clarify whether Phase 1 includes a "stop firing" signal or is truly read-only
