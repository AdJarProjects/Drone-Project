import heapq
import math
import json
import math
import mavsdk
def calc_distance(current):
    y_curr, x_curr = current
    y_goal, x_goal = goal
    y_dist = abs(y_goal - y_curr)
    x_dist = abs(x_goal - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
def get_frontier(current): ## IF FRONTIER IN VISITED SET, DONT ADD IT
    sy = current[0]
    sx = current[1]
    while sy>0 and not grid[sy][current[1]]["Walls"]["UP"] and sy < len(grid) -1 == True:
        sy += 1
        frontiers.add((sy,x))
    while sy>0 and not grid[sy][current[1]]["Walls"]["DOWN"] and sy < len(grid) -1 == True:
        sy-=1
        frontiers.add((sy,x))
    while sx>0 and not grid[current[0]][sx]["Walls"]["LEFT"] and sx < len(grid[0]) -1== True:
        sx -=1
        frontiers.add((y,sx))
    while sx>0 and not grid[current[0]][sx]["Walls"]["RIGHT"] and sx < len(grid[0]) -1 == True:
        sx+=1
        frontiers.add((y,sx))
def calc_frontier(current,frontier):
    y_curr, x_curr = current
    y_frontier, x_frontier = frontier
    y_dist = abs(y_frontier - y_curr)
    x_dist = abs(x_frontier - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
        
def det_cost(current,frontier):
    #Determine the cost of a given frontier using the Heuristic and distance traveled
    cost = calc_distance(current)+ calc_frontier(current,frontier)
    return cost

async for position in drone.telemetry.position():
    if gps_info.fix_type >= 3:  # 3D fix or better
        lat = position.latitude_deg
        lon = position.longitude_deg
        alt_abs = position.absolute_altitude_m
        alt_rel = position.relative_altitude_m
    asyncio.sleep(.1)

def frontier_calculator(current, frontierlist):
    pq = []
    for frontier in frontiers:
        heapq.heappush(pq, (detcost(current, frontier)), str(frontier))
    return heapq.pop(0)
    #to choose frontier, see which is closest to goal, to choose path from frontier, look in 4 directions, see intersection with wall, see how close that is to goal closest one we go down. then once we are within the gps spot, we check neighbors.  
def move(current,frontier):
    #move from current to frontier, A*
    return
def main():
    with open("maze_generation/maze_data.json", "r") as maze_file:
        maze_data = json.load(maze_file)
        num_rows = maze_data["rows"]
        num_cols = maze_data["cols"]
        grid = maze_data["grid"]
        start = tuple(maze_data["start"])   # JSON turns tuples into lists, convert back
        goal = tuple(maze_data["end"]) 
        cell_width = 60 # Each cell is 60cm in width and height
        cell_height = 60
        current = start
        frontiers = {}
        visited = {}
        frontiers.add(start)
        visited.add(start)
        #when the gps moves, revaluate each frontier, when we reach a frontier, we want to decide which frontier to go to next
        ## FRONTIER CALCULATOR
        while frontiers:
            frontiers.add(get_frontier(current))
            visited.add(current)
            frontiers.pop(current)
            bestfrontier = frontier_calculator(current, frontiers)
            move(current,bestfrontier)
            current = bestfrontier

            

if __name__ == "__main__":
    main()