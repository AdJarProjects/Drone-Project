"""
brain/pathfinding.py  --  Pure pathfinding. No hardware, no GPS.

Input: a Maze (start, goal, neighbors) -> output: a list of (row, col)
waypoints from start to goal. Keeping this pure means you can test and
visualize it entirely on your laptop with pyamaze before any flight.

Suggested algorithm: A* (optimal + fast on grids). BFS works too and is
simpler if every move costs the same. Red Blob Games' A* guide is the
clearest reference for the implementation.
"""

import heapq


def find_path(maze, start: tuple = None, goal: tuple = None) -> list:
    """
    Return the list of cells from start to goal inclusive, or [] if no path.
    Defaults to maze.start / maze.goal if not given.
    TODO: implement A*:
      - frontier = priority queue keyed by f = g + heuristic
      - track came_from and cost_so_far
      - expand via maze.neighbors(cell)
      - reconstruct path from goal back to start
    """
    raise NotImplementedError


def heuristic(a: tuple, b: tuple) -> float:
    """
    Admissible heuristic between two cells. Manhattan distance for 4-way
    movement; Euclidean/octile if you allow diagonals.
    """
    raise NotImplementedError


def reconstruct(came_from: dict, goal: tuple) -> list:
    """Walk came_from backwards from goal to build the ordered path."""
    raise NotImplementedError
