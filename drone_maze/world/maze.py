"""
world/maze.py  --  The maze as a grid/graph data structure.

Single source of truth for the world: which cells exist, which are walls,
where start and goal are, and which moves are legal between cells. The
pathfinder reads this; it knows nothing about GPS or hardware.

Cells are addressed as (row, col) tuples.
"""


class Maze:
    """Grid representation of the maze."""

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.start = None      # (row, col)
        self.goal = None       # (row, col)
        # TODO: choose your wall representation. Common options:
        #   - set of blocked cells, or
        #   - per-cell dict of open directions {'N','E','S','W'}.
        raise NotImplementedError

    @classmethod
    def from_file(cls, path: str) -> "Maze":
        """Load a maze definition from JSON (world/maze_data.json)."""
        raise NotImplementedError

    def to_file(self, path: str) -> None:
        """Persist the current maze back to disk (used by the editor)."""
        raise NotImplementedError

    def in_bounds(self, cell: tuple) -> bool:
        """True if (row, col) is inside the grid."""
        raise NotImplementedError

    def is_free(self, cell: tuple) -> bool:
        """True if the cell is not a wall / is passable."""
        raise NotImplementedError

    def neighbors(self, cell: tuple) -> list:
        """
        Return the legal, passable neighboring cells reachable from `cell`.
        This is the function the pathfinder calls to expand nodes.
        """
        raise NotImplementedError
