import asyncio
import json

from mavsdk import System

# Module-level state so get_frontier, det_cost, etc. can access them
grid = None
goal = None
visited = set()
frontiers = set()
sensed_open = set()
CELL_SIZE = 0.6  # 60 cm, in meters


def load_maze(path="maze_generation/maze_data.json"): #DONE
    global grid, goal
    with open(path, "r") as maze_file:
        maze_data = json.load(maze_file)
    grid = maze_data["grid"]
    start = tuple(maze_data["start"])   # JSON stores tuples as lists
    goal = tuple(maze_data["end"])
    return start, goal
def calc_distance(current): #DONE
    y_curr, x_curr = current
    y_goal, x_goal = goal
    y_dist = abs(y_goal - y_curr)
    x_dist = abs(x_goal - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
def get_frontier(current): ## IF FRONTIER IN VISITED SET, DONT ADD IT, DONE 
    cy = current[0]
    cx = current[1]
    front = []
    sy = cy
    while sy>0 and not grid[sy][cx]["Walls"]["UP"]:
        sensed_open.add(frozenset(((sy,cx),(sy-1,cx)))) 
        sy -= 1
    if (sy, cx) not in visited and (sy, cx) != current:
        front.append((sy, cx))
    sy = cy
    while len(grid) -1>sy and not grid[sy][cx]["Walls"]["DOWN"]:
        sensed_open.add(frozenset(((sy,cx),(sy+1,cx)))) 
        sy+=1
    if (sy, cx) not in visited and (sy, cx) != current:
        front.append((sy, cx))
    sx = cx
    while sx>0 and not grid[cy][sx]["Walls"]["LEFT"]:
        sensed_open.add(frozenset(((cy,sx),(cy,sx-1))))
        sx -=1
    if (cy, sx) not in visited and (cy, sx) != current:
        front.append((cy, sx))
    sx = cx
    while len(grid[0])-1>sx and not grid[cy][sx]["Walls"]["RIGHT"]:
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
        
def det_cost(current,frontier): # DONE
    #Determine the cost of a given frontier using the Heuristic and distance traveled
    cost = calc_distance(current)+ calc_frontier(current,frontier)
    return cost
def frontier_calculator(current, frontierlist): #DONE
       return min(frontierlist, key=lambda f: det_cost(current, f)) #to choose frontier, see which is closest to goal, to choose path from frontier, look in 4 directions, see intersection with wall, see how close that is to goal closest one we go down. then once we are within the gps spot, we check neighbors. 
  
async def cell_to_ned(): #TODO
    return    
async def move(drone, cell): #TODO
    north, east = cell_to_ned(cell)                      # your grid→meters transform
    await drone.offboard.set_position_ned(               # command the move
        PositionNedYaw(north, east, -1.5, 0.0)
    )
    async for pos in drone.telemetry.position_velocity_ned():   # wait for arrival
        if arrived(pos, north, east):
            break

def BFS(): #TODO
    return
async def arrived(): #TODO
    return True
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

        for cell in path[1:]:                # skip our own cell
            await move(drone, current, cell)
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

    await drone.action.arm()
    await drone.action.takeoff()
    await asyncio.sleep(5)                   # let it stabilize at altitude
    try:
        await explore(drone, start)
    finally:
        await drone.action.land()
        
        
if __name__ == "__main__":
    asyncio.run(main())