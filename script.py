import asyncio
from mavsdk import System

async def main():
    print("Starting...")
    drone = System()
    print("System created, connecting...")
    IPaddr = str(226)
    await drone.connect(system_address="udpout://192.168.1."+IPaddr+":14540")
    print("connect() returned!")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("Connected!")
            break
    await drone.action.arm()
    print("Armed!")
    await drone.action.takeoff()
    print("Took Off!")
    await asyncio.sleep(10)
    print("Landing!")
    await drone.action.land()
if __name__ == "__main__":
    asyncio.run(main())
