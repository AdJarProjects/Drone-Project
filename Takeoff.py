import asyncio
from mavsdk import System

async def main():
    drone = System()
    await drone.connect(system_address="serial:///dev/serial0:57600")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break

    print("Waiting for position health...")
    try:
        async with asyncio.timeout(60):
            async for health in drone.telemetry.health():
                if health.is_global_position_ok and health.is_home_position_ok:
                    print("Position OK.")
                    break
    except TimeoutError:
        print("No position lock — not arming.")
        return

    try:
        await drone.action.arm()
        print("Armed!")
    except Exception as e:
        print("Arm rejected:", e)
        return

    try:
        await drone.action.set_takeoff_altitude(1.5)
        await drone.action.takeoff()
        print("Takeoff commanded — hovering.")
        await asyncio.sleep(15)
    finally:
        print("Landing!")
        await drone.action.land()

asyncio.run(main())