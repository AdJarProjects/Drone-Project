import heapq
import math
import json
import math
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
def scan(current, direction):
    #Observe surroundings and determine all possible frontiers

    return
def calc_dist(current):
    y_curr, x_curr = current
    y_goal, x_goal = goal
    y_dist = abs(y_goal - y_curr)
    x_dist = abs(x_goal - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
def get_frontier(current):
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
def calc_move(current,frontier):
    y_curr, x_curr = current
    y_frontier, x_frontier = frontier
    y_dist = abs(y_frontier - y_curr)
    x_dist = abs(x_frontier - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance
        
def det_cost(current,frontier):
    #Determine the cost of a given frontier using the Heuristic and distance traveled
    cost = calc_dist(current)+ calc_move(frontier)
    return cost




async for position in drone.telemetry.position():
    if gps_info.fix_type >= 3:  # 3D fix or better
        lat = position.latitude_deg
        lon = position.longitude_deg
        alt_abs = position.absolute_altitude_m
        alt_rel = position.relative_altitude_m
    asyncio.sleep(.1)

def frontier_finder(frontierlist):
    t = 1
    #to choose frontier, see which is closest to goal, to choose path from frontier, look in 4 directions, see intersection with wall, see how close that is to goal closest one we go down. then once we are within the gps spot, we check neighbors.  
def a_star_search(grid, start, goal):
   rows, cols = len(grid), len(grid[0])
   open_list = []
   closed_set = set()
   start_node = pathfinding(start, h=heuristic(start, goal))
   heapq.heappush(open_list, (start_node.f, start_node))
   while open_list:
       _, current_node = heapq.heappop(open_list)
       if current_node.position == goal:
           path = []
           while current_node:
               path.append(current_node.position)
               current_node = current_node.parent
           return path[::-1]
       closed_set.add(current_node.position)
       for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
           neighbor_pos = (current_node.position[0] + dx, current_node.position[1] + dy)
           if not (0 <= neighbor_pos[0] < rows and 0 <= neighbor_pos[1] < cols) or grid[neighbor_pos[0]][neighbor_pos[1]] == 1:
               continue
           if neighbor_pos in closed_set:
               continue
           g_cost = current_node.g + 1
           h_cost = heuristic(neighbor_pos, goal)
           neighbor_node = Node(neighbor_pos, g=g_cost, h=h_cost, parent=current_node)
           heapq.heappush(open_list, (neighbor_node.f, neighbor_node))
   return None # No path found
# Example Usage
grid = [
   [0, 1, 0, 0],
   [0, 1, 0, 1],
   [0, 0, 0, 1],
   [1, 1, 0, 0]
]
start_coord = tuple(maze_data["start"])   # JSON turns tuples into lists, convert back
goal = (3, 3)
path = a_star_search(grid, start, goal)
print("Path:", path)