"""
safety/logger.py  --  Structured flight logging.

Records what the system saw and did each loop: state, target, command,
failsafe status. Essential for debugging autonomy after the fact, and great
material for your portfolio writeup. Write CSV (easy to plot) or JSON lines.
"""

import time
import os


class FlightLogger:
    """Appends one row per loop to a timestamped log file."""

    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self.path = None   # set in start()
        self._fh = None
        raise NotImplementedError

    def start(self) -> None:
        """
        Create log_dir if needed, open a new file named by start time,
        write the header row.
        """
        raise NotImplementedError

    def record(self, state, target, command, failsafe_status) -> None:
        """Write one row capturing this loop's inputs and outputs."""
        raise NotImplementedError

    def close(self) -> None:
        """Flush and close the file cleanly."""
        raise NotImplementedError
