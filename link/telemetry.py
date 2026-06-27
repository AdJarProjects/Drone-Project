"""
link/telemetry.py  --  Read-only MSP queries against the flight controller.

This is the refactor of your standalone drone_telemetry.py: the same
send -> receive -> process pattern, but exposed as reusable functions so
State (link/state.py) can call them on every loop instead of the code
living in a script.

NONE of these functions command movement. Reads only.
"""

# from unavlib import MSPy


def request(board, code_name: str) -> bool:
    """
    Core MSP read helper: send a request, receive the reply, decode it
    into the relevant board.<DICT>.
    send_RAW_msg -> receive_msg -> process_recv_data.
    Returns True on success.
    """
    raise NotImplementedError


def read_attitude(board) -> tuple:
    """Return (roll, pitch, yaw) in degrees. Source: MSP_ATTITUDE."""
    raise NotImplementedError


def read_gps(board) -> dict:
    """
    Return {'fix', 'numSat', 'lat', 'lon', 'alt'}.
    Source: MSP_RAW_GPS. Remember INAV stores lat/lon as int * 1e7.
    """
    raise NotImplementedError


def read_battery(board) -> dict:
    """Return {'voltage', 'amperage', 'mah_used'}. Source: MSP_ANALOG."""
    raise NotImplementedError


def read_arming_flags(board) -> list:
    """
    Return a list of human-readable arming-disable flag names
    (e.g. ['NOT_LEVEL', 'RC_LINK']). Empty list == ready to arm.
    Source: MSP_STATUS_EX + process_armingDisableFlags.
    """
    raise NotImplementedError


def read_board_info(board) -> dict:
    """Return static identity: FC variant, version, board name. Startup sanity check."""
    raise NotImplementedError
