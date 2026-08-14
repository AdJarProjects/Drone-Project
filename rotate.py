"""Rotate the sim drone to a target heading. Minimal.
 
Note: a quad can only yaw while armed and airborne (it turns by spinning
motors), so this arms, lifts just enough to rotate, turns to TARGET_YAW_DEG,
then lands. There is no way to yaw a disarmed drone on the ground.
 
Autonomous -- disable the QGC joystick and set COM_RC_IN_MODE = 4 first.
"""
 
import asyncio
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError
 
TARGET_YAW_DEG = 187.00       # heading to rotate to (0 = north)
CONNECTION     = "udp://:14540" # SITL
 
 
async def main():
    drone = System()
    await drone.connect(system_address=CONNECTION)
    async for s in drone.core.connection_state():
        if s.is_connected:
            break
    async for h in drone.telemetry.health():
        if h.is_global_position_ok and h.is_home_position_ok:
            break
 
    await drone.action.arm()
    await drone.action.takeoff()
    await asyncio.sleep(5)                    # get airborne enough to yaw
 
    async for p in drone.telemetry.position_velocity_ned():
        n, e, d = p.position.north_m, p.position.east_m, p.position.down_m
        break
 
    sp = PositionNedYaw(n, e, d, TARGET_YAW_DEG)
    await drone.offboard.set_position_ned(sp)
    try:
        await drone.offboard.start()
    except OffboardError as ex:
        print("offboard rejected:", ex._result.result)
        await drone.action.land()
        return
 
    # stream the setpoint until it's turned (a few seconds is plenty)
    for _ in range(100):                      # ~5 s at 20 Hz
        await drone.offboard.set_position_ned(sp)
        await asyncio.sleep(0.05)
 
    await drone.offboard.stop()
    await drone.action.land()
 
 
if __name__ == "__main__":
    asyncio.run(main())
 