import json
import math

with open("maze_generation/maze_data.json", "r") as maze_file:
    maze_data = json.load(maze_file)

num_rows = maze_data["rows"]
num_cols = maze_data["cols"]
grid = maze_data["grid"]
start_coord = tuple(maze_data["start"])   # JSON turns tuples into lists, convert back
end_coord = tuple(maze_data["end"])

# Each cell is 60cm in width and height
cell_width = 60
cell_height = 60

current = start_coord

known_cells = {}

goal = end_coord

dist_traveled = 0

def scan(cell, direction):
    #Observe surroundings and determine all possible frontiers

    return


def calc_dist(current):
    y_curr, x_curr = current
    y_goal, x_goal = goal
    y_dist = abs(y_goal - y_curr)
    x_dist = abs(x_goal - x_curr)
    distance = math.sqrt((y_dist ** 2) + (x_dist ** 2)) 
    return distance

def det_cost():
    #Determine the cost of a given fronteir using the Heuristic and distance traveled
    cost = 
    return


def det_frontier():

    return

def move():
    return


sync for position in drone.telemetry.position():
    lat = position.latitude_deg
    lon = position.longitude_deg
    alt_abs = position.absolute_altitude_m
    alt_rel = position.relative_altitude_m
