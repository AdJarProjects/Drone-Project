"""
tools/check_link.py  --  Quick "is the FC talking?" test. Run on the Pi.

The fastest sanity check before anything else: open the link, pull board
identity + arming flags, print, exit. If this fails, fix the connection
before touching the rest of the project.

Run:  python tools/check_link.py
"""

# from link.connection import Connection
# from link.telemetry import read_board_info, read_arming_flags


def main():
    """
    TODO:
      - open a Connection from config
      - read_board_info -> should report INAV + your F405NC
      - read_arming_flags -> print what's blocking arm
      - close cleanly
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
