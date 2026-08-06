import asyncio
import json
import math
from collections import deque
from mavsdk import System
from mavsdk.offboard import PositionNedYaw, OffboardError
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
# Module-level state so get_frontier, det_cost, etc. can access them
grid = None
goal = None
visited = set()
frontiers = set()
sensed_open = set()
origin_n = 0.0
origin_e = 0.0
theta = 0.0   # drone yaw at anchor time = maze "+forward" direction
PASS_TOL   = 1   # half a cell: close enough to count as "passed through"
SETTLE_TOL = .5   # tight arrival: only for the frontier itself
def load_maze(path=None): #DONE
    path = path or REPO_ROOT / "maze_generation" / "maze_data.json"
    global grid, goal, start, CELL_SIZE
    with open(path, "r") as maze_file:
        maze_data = json.load(maze_file)
    grid = maze_data["grid"]
    start = tuple(maze_data["start"])   # JSON stores tuples as lists
    goal = tuple(maze_data["end"])
    CELL_SIZE = maze_data["cell_dim"]
    return start, goal
def calc_distance(point): #DONE
    y_point, x_point = point
    y_goal, x_goal = goal
    y_dist = abs(y_goal - y_point)
    x_dist = abs(x_goal - x_point)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
def get_frontier(current): ## IF FRONTIER IN VISITED SET, DONT ADD IT, DONE 
    cy = current[0]
    cx = current[1]
    front = []
    sy = cy
    while sy>0 and not grid[sy][cx]["walls"][0]:
        sensed_open.add(frozenset(((sy,cx),(sy-1,cx)))) 
        sy -= 1
    if (sy, cx) not in visited and (sy, cx) != current:
        front.append((sy, cx))
    sy = cy
    while len(grid) -1>sy and not grid[sy][cx]["walls"][1]:
        sensed_open.add(frozenset(((sy,cx),(sy+1,cx)))) 
        sy+=1
    if (sy, cx) not in visited and (sy, cx) != current:
        front.append((sy, cx))
    sx = cx
    while sx>0 and not grid[cy][sx]["walls"][2]:
        sensed_open.add(frozenset(((cy,sx),(cy,sx-1))))
        sx -=1
    if (cy, sx) not in visited and (cy, sx) != current:
        front.append((cy, sx))
    sx = cx
    while len(grid[0])-1>sx and not grid[cy][sx]["walls"][3]:
        sensed_open.add(frozenset(((cy,sx),(cy,sx+1))))
        sx+=1
    if (cy, sx) not in visited and (cy, sx) != current:
        front.append((cy, sx))
    return front
def calc_frontier(current,frontier): # DONE 
    y_curr, x_curr = current
    y_frontier, x_frontier = frontier
    y_dist = abs(y_frontier - y_curr)
    x_dist = abs(x_frontier - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
async def capture_anchor(drone):
    global origin_e,origin_n,theta
    async for pos in drone.telemetry.position_velocity_ned():
        origin_n, origin_e = pos.position.north_m, pos.position.east_m
        break
    async for att in drone.telemetry.attitude_euler():
        theta = math.radians(att.yaw_deg)
        break
    
def det_cost(current,frontier): # DONE
    #Determine the cost of a given frontier using the Heuristic and distance traveled
    cost = calc_distance(frontier)+ calc_frontier(current,frontier)
    return cost
def frontier_calculator(current, frontierlist): #DONE
       return min(frontierlist, key=lambda f: det_cost(current, f)) #to choose frontier, see which is closest to goal, to choose path from frontier, look in 4 directions, see intersection with wall, see how close that is to goal closest one we go down. then once we are within the gps spot, we check neighbors. 
  
def cell_to_ned(cell): #DONE
    forward = (cell[0] - start[0])*CELL_SIZE
    right = (cell[1] - start[1])*CELL_SIZE
    north = origin_n + forward * math.cos(theta) - right * math.sin(theta)
    east  = origin_e + forward * math.sin(theta) + right * math.cos(theta)
    return north, east
async def move(drone, cell, settle): 
    north, east = cell_to_ned(cell)
    await drone.offboard.set_position_ned(
        PositionNedYaw(north, east, -1.5, math.degrees(theta)))
    tol = SETTLE_TOL if settle else PASS_TOL
    try:
        async with asyncio.timeout(7):
            async for pos in drone.telemetry.position_velocity_ned():
                if arrived(pos,north,east,tol):
                    return
    except TimeoutError:
        print(f"move to {cell}: timed out, continuing")

def arrived(pos,north,east,tol): #DONE
    dn = pos.position.north_m - north ##distance from its current position to the goal
    de = pos.position.east_m - east
    return math.hypot(dn,de) < tol
async def connect_drone(): #DONE
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14540")
    # await drone.connect(system_address="serial:///dev/serial0:57600")
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
        print("No position lock after 60 s — not arming.")
        return None          # explicit failure signal
    return drone      
def BFS(startcell, goalcell): #Done
    """Breadth-first search from startcell to goalcell.
    Returns the shortest path as a list of cells [startcell, ..., goalcell],
    or None if goalcell is unreachable."""
    queue = deque([startcell])
    came_from = {startcell: None}   # visited-set + parent pointers in one

    while queue:
        cell = queue.popleft()

        if cell == goalcell:
            # reconstruct path by walking parents back to the start
            path = []
            while cell is not None:
                path.append(cell)
                cell = came_from[cell]
            return path[::-1]        # reverse: start -> goal

        for n in neighbors(cell):
            if n not in came_from:   # first visit is the shortest route
                came_from[n] = cell
                queue.append(n)

    return None                      # queue exhausted, goal unreachable


def neighbors(cell): #Done
    """Adjacent cells whose passage the drone has actually sensed."""
    cy, cx = cell
    candidates = ((cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1))
    return [n for n in candidates if frozenset((cell, n)) in sensed_open] #check if the cell to canadiate passage is in the sensed_open
async def explore(drone, start): #DONE
    current = start
    visited.add(current)
    frontiers.update(get_frontier(current))

    while frontiers:
        bestfrontier = frontier_calculator(current, frontiers)
        path = BFS(current, bestfrontier)

        if not path:
            frontiers.discard(bestfrontier)  # unreachable, drop it
            continue

        for i, cell in enumerate(path[1:], start=1):
            await move(drone, cell, settle=(i == len(path) - 1))
            current = cell
            if current not in visited:
                visited.add(current)
                frontiers.discard(current)
                frontiers.update(get_frontier(current))
            if current == goal:                  # optional: stop when goal reached
                print("Goal reached!")
                return

    print("Exploration complete — no frontiers left.")

async def main(): #DONE
    start, _ = load_maze()
    drone = await connect_drone()
    if drone is None:
        return
    
    try:
        await drone.action.arm()
    except Exception as e:
        print("Arm rejected:", e)
        return
    await capture_anchor(drone)
    await drone.action.set_takeoff_altitude(1.5)
    await drone.action.takeoff()
    await asyncio.sleep(8)
    try:
        for _ in range(20):
            await drone.offboard.set_position_ned(
                PositionNedYaw(origin_n, origin_e, -1.5, math.degrees(theta)))
            await asyncio.sleep(0.05)
        try:
            await drone.offboard.start()
        except OffboardError as error:
            print(f"Offboard start failed: {error._result.result}")
            return
        await explore(drone, start)
        await drone.offboard.stop()
    finally:
        await drone.action.land()
    await asyncio.sleep(5)                   # let it stabilize at altitude
        
        
if __name__ == "__main__":
    asyncio.run(main())