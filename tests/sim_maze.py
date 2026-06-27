"""
tests/sim_maze.py  --  Visualize the pathfinder with pyamaze. Laptop only.

This is your "watch it solve" harness and the safe sandbox for the entire
maze-solving half of the project -- no aircraft involved. Build a maze,
run YOUR find_path on it, and animate the agent following the result.

Run:  python tests/sim_maze.py
"""

# from pyamaze import maze, agent, COLOR
# from world.maze import Maze
# from brain.pathfinding import find_path


def build_pyamaze_grid():
    """
    Create a pyamaze maze for visualization. Note pyamaze uses 1-based
    (row, col) with its own wall model -- you'll translate between it and
    your world.Maze representation here.
    TODO.
    """
    raise NotImplementedError


def run_simulation():
    """
    1. build a maze (pyamaze + your Maze in sync)
    2. path = find_path(your_maze)
    3. translate path to pyamaze cell coords
    4. agent + tracePath to animate
    5. m.run()
    TODO.
    """
    raise NotImplementedError


if __name__ == "__main__":
    run_simulation()
