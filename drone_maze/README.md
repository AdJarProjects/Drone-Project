# Autonomous Maze Drone

Pi-companion-computer controller that solves a virtual maze and flies the
path on an INAV flight controller via MSP (uNAVlib).

- **Pi 4** companion computer → **AERO SELFIE F405NC** running **INAV 9.x**
- Pathfinding + maze live-editing run on a laptop; flight code runs on the Pi.
- INAV handles stabilization (gyro loop). The Pi only does **guidance**.

## Architecture

    link/    talk to the flight controller (MSP)
    world/   the maze + cell<->GPS mapping
    brain/   pathfinding, mission sequencing, guidance
    safety/  failsafe watchdog + flight logging
    tests/   laptop-side validation (no hardware) + pyamaze sim
    tools/   link check + mode-config capture

`main.py` is the runtime loop that wires it together. `config.yaml` holds
every tunable constant.

## Build order (recommended)

1. **Brain in sim, on your laptop.** Implement `world/maze.py`,
   `brain/pathfinding.py`, `world/editor.py`. Validate with
   `tests/test_pathfinding.py` and watch it solve in `tests/sim_maze.py`
   (pyamaze). No aircraft needed.
2. **Geo math.** Implement `world/geo.py` and `brain/guidance.py`; verify
   with `tests/test_geo.py`.
3. **Link, read-only.** Implement `link/connection.py`, `link/telemetry.py`,
   `link/state.py`. Confirm with `tools/check_link.py` on the Pi over USB.
4. **Control — props OFF.** Implement `link/control.py`, `link/arming.py`.
   Test arm/disarm and a single command with no props, transmitter ready.
5. **Failsafe.** Implement `safety/failsafe.py`. Verify every trigger hands
   control back to the transmitter.
6. **Integrate.** Wire `main.py`, run `safety/logger.py`. Bench first, then
   — outdoors with GPS, transmitter as override — a real waypoint run.

## Setup

### On the Pi
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### INAV Configurator
- Ports tab: enable **MSP** on the UART you use (USB VCP has it by default).
- Receiver tab (only when ready for control): **MSP RX**, AETR order.
- Build/enable **MSP RC Override** and configure **failsafe for MSP RC-link loss**.

## Safety

- Always test props-off until arm/disarm and failsafe are proven.
- Keep the FlySky transmitter bound and able to take over instantly.
- NEO-6M GPS is ~2.5 m outdoors and unusable indoors — size your maze
  accordingly or use a different positioning source.
- `drone.service` auto-starts on boot; only enable it after full testing.
