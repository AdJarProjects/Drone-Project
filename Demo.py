import asyncio
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed, OffboardError

async def main():
    print("Starting...")
    drone = System()
    print("System created, connecting...")
    IPaddr = str(226)
    await drone.connect(system_address="udpout://192.168.1."+IPaddr+":14540") 
    '''Will become: await drone.connect(system_address="serial:///dev/serial0:57600") once we recive the FC'''
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
    print("START and SPEED: 1N")
    # Send setpoints FIRST, before start() — PX4 needs to already be receiving
    # them or it rejects the mode switch with NO_SETPOINT_SET -- CLAUDE

    print("Priming offboard setpoint...")
    for _ in range(10):
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
        await asyncio.sleep(0.1)
    try:
        await drone.offboard.start() #error handling incase the drone offboard mode doesnt work
    except OffboardError as error:
        print(f"Starting offboard failed: {error._result.result}") 
        await drone.action.land()
        return
    for _ in range(100):
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(1,0,0,0))
        await asyncio.sleep(.1)
    print("Speed: -1N")
    for _ in range(100):
        await drone.offboard.set_velocity_body(VelocityBodyYawspeed(-1,0,0,0))
        await asyncio.sleep(.1)
    print("STOP OFFBOARD")
    await drone.offboard.stop()
    print("Landing!")
    await drone.action.land()
if __name__ == "__main__":
    asyncio.run(main())
