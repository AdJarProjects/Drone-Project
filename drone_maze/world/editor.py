"""
world/editor.py  --  Live editing of the maze.

Lets you change walls/start/goal while the system runs. Simplest robust
approach: watch maze_data.json for changes and reload + re-plan when it's
edited. (Alternatives: a small GUI or keyboard controls -- pick one and
implement it here so the rest of the app is unaffected.)
"""


class MazeEditor:
    """Watches the maze file and signals when it changes."""

    def __init__(self, maze, data_file: str, on_change=None):
        """
        maze:      the Maze instance to keep in sync
        data_file: path to watch
        on_change: callback invoked after a successful reload
                   (e.g. main.py re-runs find_path here)
        """
        self.maze = maze
        self.data_file = data_file
        self.on_change = on_change
        self._last_mtime = None
        raise NotImplementedError

    def poll(self) -> bool:
        """
        Called each loop. If the file changed on disk, reload the maze and
        fire on_change. Returns True if a reload happened.
        TODO: compare file mtime; on change call maze.from_file and on_change.
        """
        raise NotImplementedError

    def set_cell(self, cell: tuple, blocked: bool) -> None:
        """Programmatically toggle a wall and persist (for GUI/keyboard mode)."""
        raise NotImplementedError
