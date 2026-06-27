"""
tests/test_pathfinding.py  --  Validate the pathfinder on known mazes.

Runs entirely on your laptop, no hardware. Build a small Maze with a known
solution and assert find_path returns a valid, connected path from start
to goal that avoids walls.
"""

# from world.maze import Maze
# from brain.pathfinding import find_path


def test_straight_line():
    """Empty grid: path should exist and be the optimal length. TODO."""
    raise NotImplementedError


def test_blocked_has_no_path():
    """Goal walled off entirely: find_path returns []. TODO."""
    raise NotImplementedError


def test_path_is_connected_and_legal():
    """
    Every step in the returned path is a legal neighbor of the previous
    cell and is_free. TODO.
    """
    raise NotImplementedError


if __name__ == "__main__":
    # Allow running with plain `python tests/test_pathfinding.py`,
    # or use pytest.
    test_straight_line()
    test_blocked_has_no_path()
    test_path_is_connected_and_legal()
    print("All pathfinding tests passed.")
