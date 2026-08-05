import asyncio
from mavsdk import System

async def main():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected to SITL!")
            break
    async for health in drone.telemetry.health():
        print("Global position OK:", health.is_global_position_ok)
        break

asyncio.run(main())