# KilnWatch — Product Overview

## Purpose
KilnWatch is a kiln controller system that will support any standard electric kiln and provide both programming and monitoring of operation for firing or annealing glass, ceramics, and metals.
The system will read up to 4 thermocouples in one or more kilns and be able to control heating elements for single or multi-zone temperature regulation.
It will allow a user to program a firing schedule with 1 to 8 segments with an optional delayed start time. Each segment will provide for a ramp rate, target temperature, hold time at target temperature, and ability to alert at transitions such as start of ramp, start of hold, end of segment, temperature outside of limits, and possibly other states to be determined.
It will store time-series data and display it as numerical values and real-time graphs.
It will provide a connected interface with either mechanical buttons or touchscreen and monitor and will provide a web interface for remote monitoring, configuration, and control.
The project will be built and tested in several phases beginning with a simple monitoring and reporting system.

## Background
The kiln currently in use is a Skutt KM-818 ceramic kiln with its proprietary controller designed for firing ceramics. In addition to its stock thermocouple it has 3 K-type thermocouples inserted in the view ports for monitoring temperature at 3 different heights in the kiln. A secondary kiln is a small Evenheat knife maker kiln.

The shop is not co-located with the operator's home or workplace. Remote monitoring — including
the ability to check status, adjust configurations, receive notifications and alerts, and terminate a firing — are primary
requirements.

## Core Requirements (Phase 1 — Monitor & Log)

### Thermocouple Input
- Read 1–4 K-type thermocouples simultaneously
- Each thermocouple is user-labeled (e.g., "Top Zone", "Bottom Zone", "Shelf 1")
- Labels appear in stored data and on graphs
- Hardware: MAX31856 breakout boards, one per thermocouple, on shared SPI bus of a Raspberry Pi model 4
- Each thermocouple can be assigned, via configuration, to a kiln (e.g., TCs 1–3 → Skutt 818, TC 4 → Evenheat),
  allowing more than one kiln to be monitored; the user selects which kiln to view at a given time. See
  "Multi-Kiln Monitoring" under Future Phase for what's still undefined here.

### Units
- Default display and input unit: Fahrenheit (operator's local convention)
- User-configurable to Celsius for both display and program entry
- Internal storage/computation units follow whatever a library or hardware driver requires (e.g., the MAX31856
  driver returns Celsius natively) — convert to the user's preferred unit only at the UI boundary, not
  internally. See tech.md Decisions Log.

### Data Logging
- Log all thermocouple readings with timestamps to persistent storage
- Configurable sample interval (default: 30 seconds; range: 5s–5min)
- Storage on local SD card; offload/backup to networked computer supported
- SQLite database preferred for query flexibility

### Display
- On-device display: Raspberry Pi 7" official touchscreen or similar (HDMI/DSI)
- Real-time time-series graph of all active thermocouples
- Firing program overlay on graph (ramp/hold segments as stepped lines)
- On-device touch UI for viewing data and entering/editing firing programs
- Emergency stop: a GPIO output can trigger an external contactor or circuit breaker to cut all power to the
  kiln — an on/off power cutoff, not modulation of the heating elements. The GPIO signal will be made
  available in Phase 1; the external wiring/hardware implementation is TBD (see tech.md GPIO allocation).

### Web Interface
- Hosted on the device (Flask or FastAPI)
- Accessible from home/work over the internet (not just LAN)
- Real-time or near-real-time graph display (auto-refreshing or WebSocket)
- Remote ability to: view current temps, view programmed segments, start/stop logging session
- Remote ability to trigger the same GPIO-based emergency power cutoff described above
- Authentication required (this device is internet-accessible)

### Firing Program Entry
- A firing program consists of 1–8 segments
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
- Selectable standard programs and saved programs from previous sessions
- Drive solid-state relays (SSR) to control heating elements
- PID or ramp-and-soak control loop per zone
- Emergency shutoff logic (overtemp, sensor fault, runaway detection)
- All firing programming done on KilnWatch; Skutt controller bypassed
- Multi-Kiln Monitoring: Phase 1 lets TCs be grouped into more than one kiln for monitoring, but several
  things about that are still undefined and need deciding before/while control is added:
  - Whether EStop is one shared GPIO line covering all defined kilns, or a dedicated EStop line is needed per
    kiln (relevant if each kiln has its own contactor)
  - Whether/how kiln control (SSR, PID) extends to more than one kiln concurrently

## Non-Goals (Phase 1)
- No control of heating elements — the Phase 1 emergency stop is a binary power cutoff via an external
  contactor/breaker, not modulation of the elements themselves
- No integration with Skutt proprietary protocol
- No cloud data storage (local only in Phase 1)
- No per-kiln control logic — Phase 1 "kilns" are just a logical grouping of thermocouples for monitoring
  (see Thermocouple Input); actual kiln control is Future Phase

## Operator Context
- Operator: experienced systems/network engineer, moderate Python, moderate electronics background
- Primary interface: touchscreen on device at the kiln
- Secondary interface: web browser from home or mobile device while away from shop
- Prefers direct technical responses; can ask follow-up questions on unfamiliar details

## Open Items — UPDATE THIS SECTION AS VISION EVOLVES
- [ ] Confirm remote access method (Cloudflare Tunnel vs. DDNS + port-forward)
- [ ] Confirm display choice (7" DSI touchscreen vs. HDMI)
- [ ] Confirm on-device UI approach (Chromium kiosk vs. Python GUI)
- [ ] EStop GPIO pin: TBD, can be any available GPIO pin
- [ ] EStop scope: one shared line for all defined kilns, or one per kiln (see Future Phase — Kiln Control)
