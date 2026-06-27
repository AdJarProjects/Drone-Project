"""
link/connection.py  --  Owns the single MSP serial connection to the FC.

Everything that talks to the flight controller goes through ONE Connection
instance. The FC's UART allows only one connection at a time, so this class
centralizes open/close/reconnect and hands the live board handle to the
telemetry and control modules.
"""

# from unavlib import MSPy


class Connection:
    """Manages the lifetime of the MSP serial link."""

    def __init__(self, serial_port: str, baud_rate: int = 115200):
        """Store connection params. Does NOT open the port yet."""
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.board = None  # the MSPy handle once connected
        raise NotImplementedError

    def open(self) -> bool:
        """
        Open the serial port and connect via MSPy.
        Returns True on success, False on failure.
        TODO: instantiate MSPy, handle the connect()==1 failure quirk.
        """
        raise NotImplementedError

    def close(self) -> None:
        """Close the serial port cleanly."""
        raise NotImplementedError

    def reconnect(self) -> bool:
        """Attempt to re-open after a dropped link. Returns success."""
        raise NotImplementedError

    def is_connected(self) -> bool:
        """Return True if the link is currently open and healthy."""
        raise NotImplementedError
