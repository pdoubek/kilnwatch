# KilnWatch — Pi Deployment Guide

## 1. Flash and Prep the Pi

Use Raspberry Pi Imager. Select **Raspberry Pi OS (64-bit)**:
- Lite if using Chromium kiosk or headless web-only
- Full Desktop if using a Python GUI

Configure SSH and WiFi in Imager's Advanced Settings before flashing.

After first boot:
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y git python3-pip python3-venv python3-dev
```

## 2. Enable SPI

```bash
sudo raspi-config
# Interface Options → SPI → Enable
sudo reboot
```

Verify:
```bash
ls /dev/spidev*    # should show /dev/spidev0.0 and /dev/spidev0.1
```

## 3. Wire the MAX31856 Boards

All boards share MOSI/MISO/SCLK. Each needs its own CS wire:

| Signal | Pi BCM GPIO | Pi Header Pin |
|--------|-------------|---------------|
| MOSI   | GPIO 10     | Pin 19        |
| MISO   | GPIO 9      | Pin 21        |
| SCLK   | GPIO 11     | Pin 23        |
| CS-TC1 | GPIO 8      | Pin 24        |
| CS-TC2 | GPIO 7      | Pin 26        |
| CS-TC3 | GPIO 25     | Pin 22        |
| CS-TC4 | GPIO 24     | Pin 18        |
| 3.3V   | 3.3V        | Pin 1 or 17   |
| GND    | GND         | Pin 6, 9, etc.|

If noise/fault errors occur: solder a 100nF cap across each board's TC+ and TC- terminals.

## 4. Install KilnWatch

```bash
cd ~
git clone https://github.com/YOUR_USERNAME/kilnwatch.git
cd kilnwatch
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env            # set WEB_USERNAME, WEB_PASSWORD_HASH, SECRET_KEY
cp config/settings.example.toml config/settings.toml   # set TC labels and pins
python scripts/init_db.py
```

## 5. Install and Start the systemd Service

```bash
sudo cp deploy/kilnwatch.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable kilnwatch
sudo systemctl start kilnwatch
```

Check status and logs:
```bash
sudo systemctl status kilnwatch
journalctl -u kilnwatch -f
```

## 6. Remote Access

### Option A — Cloudflare Tunnel (recommended)
No port forwarding required. Works through NAT and most firewalls.

Install cloudflared on the Pi, log into Cloudflare Zero Trust, create a tunnel
pointing to `localhost:5000`. You get a stable public HTTPS URL.
Full setup: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/

### Option B — DDNS + Port Forward
1. Set up DDNS (DuckDNS, No-IP) pointed at the shop's public IP
2. On the shop router: forward TCP port 5000 to the Pi's local IP
3. Give the Pi a static local IP via DHCP reservation
4. Access: `http://your-name.duckdns.org:5000`

Option A is preferred — avoids exposing a port and adds Cloudflare access controls.

## 7. Updating the Pi

From your dev machine:
```bash
git push origin main
```

On the Pi:
```bash
cd ~/kilnwatch
git pull
# If requirements changed:
source venv/bin/activate && pip install -r requirements.txt
sudo systemctl restart kilnwatch
```

## 8. Kiosk Mode (Touchscreen)

Requires Pi OS with Desktop installed.

```bash
sudo apt install -y chromium-browser unclutter
```

Create `~/.config/autostart/kilnwatch-kiosk.desktop`:
```ini
[Desktop Entry]
Type=Application
Name=KilnWatch Kiosk
Exec=chromium-browser --kiosk --noerrdialogs --disable-infobars --disable-session-crashed-bubble http://localhost:5000
```

The browser opens KilnWatch full-screen at boot. The web UI doubles as the
on-device touchscreen interface — no separate GUI codebase needed.
