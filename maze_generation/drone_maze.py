#Libraries
from mavsdk import System
import random
from PIL import Image, ImageDraw, ImageOps
import os
import json
import math
import asyncio

# INITIALIZATION

#Ask the user for the amount of rows and columns, must be greater than 2
rows, cols = 0, 0
while rows < 3 or cols < 3:
    rows = int(input("Number of rows: "))
    cols = int(input("Number of columns: "))
    if rows < 3:
        print("Number of rows must be greater than 2.")
    if cols < 3:
        print("Number of columns must be greater than 2.")

#Set to true or false depending on if you are using the drone or not
using_drone = False

# Set the status of walls to true for all tiles
# [Top, Bottom, Left, Right]
grid = [[{"walls": [True, True, True, True]} for _ in range(cols)] for _ in range(rows)]

#COORDINATE GRID CREATION

# Create the grid of coordinates based on the starting location
coord_grid = [[None for _ in range(cols)] for _ in range(rows)] #initialized grid of GPS coordinates for the maze
cell_dim = .60 #Cell length and width in m

#Set if the drone is not being used
set_coord = (0, 0)
set_bearing = math.radians(0)

#Ensure that the drone is running, then get the starting coordinate and bearing from the FC
async def get_drone_origin():
    drone = System()
    await drone.connect(system_address="") #Depends on our address

    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            break

    async for drone_pos in drone.telemetry.position():
        start_coord = (drone_pos.latitude_deg, drone_pos.longitude_deg)
        break

    async for drone_br in drone.telemetry.attitude_euler():
        bearing = math.radians(drone_br.yaw_deg % 360)  #Starting cardinal direction of the front of the drone
        break
    return start_coord, bearing

# Use flight controller if drone is being used, if not use inputted data
if using_drone:
    start_coord, bearing = asyncio.run(get_drone_origin())
else:
    start_coord, bearing = set_coord, set_bearing


#Flat Earth Approximation to find coordinates for smaller distances
def find_coord(cell_idx, cell_dim, start_coord, bearing):
    start_lat, start_long = start_coord
    row, col = cell_idx

    forward = row * cell_dim
    right = col * cell_dim

    dlat = (forward * math.cos(bearing) - right * math.sin(bearing)) / 111320.0
    dlong = (forward * math.sin(bearing) + right * math.cos(bearing)) / (111320.0 * math.cos(math.radians(start_lat)))
    fin_coord = start_lat + dlat, start_long + dlong
    return fin_coord

#Find the coordinate for each cell in our grid
for r in range(rows):
    for c in range(cols):
        coord_grid[r][c] = find_coord((r, c), cell_dim, start_coord, bearing)


#Create a set of all cells in the bounds inputted
all_cells = {(y, x) for y in range(rows) for x in range(cols)}

#Index of the directions used to carve walls
directions = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
wall_idx = {"Up": 0, "Down": 1, "Left": 2, "Right": 3}

# Generate a random start coordinate on the top row
start = (0, random.randint(1, cols - 2))
y_start, x_start = start

#Generate a random end coordinate on the bottom row
end = ((rows - 1), random.randint(1, cols - 2))
y_end, x_end = end


#Set the current coordinate to the start
current = start
y_curr, x_curr = current

#Initialize the dictionary of all visited cells
visited = {start}

#initialize the set of the stack of cells (The current path being explored)
stack = [start]

# Function to carve the walls when moving from one cell to another
def open_walls(grid, cell, direction):
    y_cord, x_cord = cell
    dy, dx = directions[direction]

    #open wall of current cell
    grid[y_cord][x_cord]["walls"][wall_idx[direction]] = False

    #Go to next cell and open wall
    y_fin, x_fin = y_cord + dy, x_cord + dx
    opp_wall = wall_idx[direction] ^ 1
    grid[y_fin][x_fin]["walls"][opp_wall] = False

# Function to make sure that you can move into the selected neighboring cell
def validate_move(visited, current, direction):
    dy, dx = directions[direction]
    new_current = (dy + current[0], dx + current[1])
    new_y, new_x = new_current
    if new_y < 0 or new_y > (rows - 1) or new_x < 0 or new_x > (cols - 1):
        return 0
    elif new_current in visited:
        return 0
    else:
        return 1

# Function to check how many neighbors are possible to move in to
def check_neighbors(current):
    options = 0
    for direction in directions:
        options += validate_move(visited, current, direction)
    return options

# Function to move into a random, validated, neighboring cell
def random_move(current, grid, directions):
    while True:
        direction = random.choice(list(directions)) #pick a random connected edge
        # Validate move
        if validate_move(visited, current, direction):
            #remove walls
            dy, dx = directions[direction]
            new_current = (dy + current[0], dx + current[1])
            open_walls(grid, current, direction)
            current = new_current
            visited.add(new_current)
            stack.append(new_current)
            return new_current

#Function to backtrack into the stack if there are no possible neighbors
def backtrack():
    neighbors = 0
    current = stack[-1]
    while neighbors == 0:
        stack.pop()
        current = stack[-1]
        neighbors = check_neighbors(current)
    return current

# Generates the maze by going through and opening walls until all cells are visited
def generate(current):
    while not all_cells.issubset(visited):
    #Check Neighbors for move
        valid_neighbors = check_neighbors(current)
        if valid_neighbors > 0:
            current = random_move(current, grid, directions)
        else:
            current = backtrack()
    return

generate(current)

#Set the entrence and exit to be open
grid[y_end][x_end]["walls"][1] = False
grid[y_start][x_start]["walls"][0] = False

# Create JSON so that solving code is able to read maze

folder = r"C:\Users\adamj\OneDrive\Documents\Professional\Portfolio\Drone Project\Code_Files\Drone-Project\maze_generation"

maze_data = {
    "rows": rows,
    "cols": cols,
    "grid": grid,
    "start": start,
    "end": end,
    "coord_grid": coord_grid,
    "origin": start_coord,
    "start_bearing": bearing
}

with open(os.path.join(folder, "maze_data.json"), "w") as f:
    json.dump(maze_data, f)

#Print start and end coordinates
print("The Maze Entrence is", start)
print("The Maze Exit is", end)

# Maze image creation
cell_img_size = 20

img = Image.new("RGB", (cols * cell_img_size + 1, rows * cell_img_size + 1), "white")
draw = ImageDraw.Draw(img)

for y in range(rows):
    for x in range(cols):
        walls = grid[y][x]["walls"]
        px, py = x * cell_img_size, y * cell_img_size

        top, bottom, left, right = walls

        if top:
            draw.line([(px, py), (px + cell_img_size, py)], fill="black")
        if bottom:
            draw.line([(px, py + cell_img_size), (px + cell_img_size, py + cell_img_size)], fill="black")
        if left:
            draw.line([(px, py), (px, py + cell_img_size)], fill="black")
        if right:
            draw.line([(px + cell_img_size, py), (px + cell_img_size, py + cell_img_size)], fill="black")
img = ImageOps.expand(img, border=10, fill="white")

#Saving and displaying image

os.makedirs(folder, exist_ok=True)
img.save(os.path.join(folder, "maze.png"))
img.show()