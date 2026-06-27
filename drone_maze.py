from unavlib import MSPy

from pyamaze import maze, agent

# Instantiate a 15x15 maze
m = maze(15, 15)
m.CreateMaze(loopPercent=50) # Generates paths with some loops

# Add an animated agent to navigate it
a = agent(m, footprints=True)
m.run()