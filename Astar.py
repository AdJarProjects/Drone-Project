import heapq
import math
class Node:
   def __init__(self, position, g=0, h=0, parent=None):
       self.position = position
       self.g = g # Cost from start to this node
       self.h = h # Heuristic cost to goal
       self.f = g + h # Total cost
       self.parent = parent
def heuristic(currentd, goald):
   return math.sqrt(math.pow((goald[0] - currentd[0]),2) + math.pow((goald[1] - currentd[1]),2))
def frontier_maker(currentposition,grid):
    t = 1
def frontier_finder(frontierlist):
    t = 1
    #to choose frontier, see which is closest to goal, to choose path from frontier, look in 4 directions, see intersection with wall, see how close that is to goal closest one we go down. then once we are within the gps spot, we check neighbors.  
def a_star_search(grid, start, goal):
   rows, cols = len(grid), len(grid[0])
   open_list = []
   closed_set = set()
   start_node = Node(start, h=heuristic(start, goal))
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
start = (0, 0)
goal = (3, 3)
path = a_star_search(grid, start, goal)
print("Path:", path)