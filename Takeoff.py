import asyncio
from mavsdk import System
from mavsdk.offboard import Attitude, OffboardError

async def status(drone):
    async for s in drone.telemetry.status_text():
        print(f"{s.type}: {s.text}")

async def main():
    drone = System()
    await drone.connect(system_address="serial:///dev/serial0:921600")
    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    asyncio.ensure_future(status(drone))

    await drone.action.arm()
    print("armed")

    await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.40))
    try:
        await drone.offboard.start()
    except OffboardError as e:
        print("offboard rejected:", e._result.result)
        await drone.action.disarm()
        return
    print("offboard — flip the kill switch")

    for _ in range(300):
        await drone.offboard.set_attitude(Attitude(0.0, 0.0, 0.0, 0.40))
        await asyncio.sleep(0.05)

    await drone.offboard.stop()
    await drone.action.disarm()

asyncio.run(main())