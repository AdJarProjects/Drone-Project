#!/usr/bin/env python3
"""
Autonomous position-hold hover.

Sequence: connect -> wait for a trusted position estimate -> arm -> take off
to TARGET_ALT -> lock the current NED point and hold it with offboard setpoints
for HOLD_S -> land -> disarm.

Unlike plain Hold/Loiter mode, this actively commands a fixed NED position, so
PX4 fights drift/wind to keep it on the spot instead of just holding altitude
and letting it wander.

Keep the transmitter in hand. Your RC override (SwC) and kill switch (SwD) work
throughout -- takeoff, offboard, and land are all auto/offboard modes covered by
COM_RC_OVERRIDE, so a switch flip takes control back immediately.
"""

import asyncio
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError

# ---- tunables -------------------------------------------------------------
CONNECTION = "serial:///dev/serial0:921600"  # Pi UART. Use udp://:14540 for SITL.
TARGET_ALT = 2.0     # metres above takeoff point
HOLD_S     = 15.0    # seconds to hold position
ALT_TOL    = 0.3     # "reached altitude" band, metres
SETPOINT_HZ = 20     # offboard setpoint rate (PX4 needs > 2 Hz)
# ---------------------------------------------------------------------------


async def print_status(drone):
    async for s in drone.telemetry.status_text():
        print(f"[{s.type}] {s.text}")


async def get_yaw(drone):
    """Current heading in degrees, so we hold heading instead of snapping to 0."""
    async for att in drone.telemetry.attitude_euler():
        return att.yaw_deg


async def main():
    drone = System()
    print("connecting...")
    await drone.connect(system_address=CONNECTION)

    async for state in drone.core.connection_state():
        if state.is_connected:
            print("connected")
            break

    asyncio.ensure_future(print_status(drone))

    # --- gate on a real position estimate before arming --------------------
    # takeoff + offboard position need global position and home set. This loop
    # blocks until the EKF is happy; if it hangs here, that's GPS/heading, not code.
    print("waiting for position estimate (GPS + home)...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("position OK")
            break

    # --- arm + takeoff -----------------------------------------------------
    await drone.action.set_takeoff_altitude(TARGET_ALT)

    print("arming")
    await drone.action.arm()

    print(f"taking off to {TARGET_ALT:.1f} m")
    await drone.action.takeoff()

    async for pos in drone.telemetry.position():
        if pos.relative_altitude_m >= TARGET_ALT - ALT_TOL:
            break

    # let it settle a beat so the captured hold point isn't mid-climb
    await asyncio.sleep(2.0)

    # --- capture the point to hold -----------------------------------------
    async for p in drone.telemetry.position_velocity_ned():
        n = p.position.north_m
        e = p.position.east_m
        d = p.position.down_m
        break
    yaw = await get_yaw(drone)
    print(f"holding NED (n={n:.2f}, e={e:.2f}, d={d:.2f}), yaw={yaw:.0f}")

    hold = PositionNedYaw(n, e, d, yaw)

    # --- enter offboard: PX4 requires setpoints already flowing ------------
    await drone.offboard.set_position_ned(hold)
    try:
        await drone.offboard.start()
    except OffboardError as e:
        print("offboard rejected:", e._result.result, "-- landing")
        await drone.action.land()
        return

    print(f"position hold for {HOLD_S:.0f} s")
    ticks = int(HOLD_S * SETPOINT_HZ)
    for _ in range(ticks):
        await drone.offboard.set_position_ned(hold)   # re-send to keep stream alive
        await asyncio.sleep(1.0 / SETPOINT_HZ)

    # --- hand back to autopilot and land -----------------------------------
    await drone.offboard.stop()

    print("landing")
    await drone.action.land()

    async for in_air in drone.telemetry.in_air():
        if not in_air:
            break
    print("landed")

    try:
        await drone.action.disarm()   # usually auto-disarms on land
    except Exception:
        pass


if __name__ == "__main__":
    asyncio.run(main())