"""
link/state.py  --  Cached snapshot of the aircraft's current state.

The brain shouldn't block on serial reads. State.update() pulls fresh
telemetry once per loop and stores it; everything else reads the cached
attributes. Also timestamps each update so Failsafe can detect a stale link.
"""

import time
# from link import telemetry


class State:
    """Holds the latest known aircraft state."""

    def __init__(self, connection):
        """Keep a reference to the open Connection."""
        self.connection = connection
        self.attitude = (0.0, 0.0, 0.0)   # roll, pitch, yaw (deg)
        self.position = None              # dict: fix, numSat, lat, lon, alt
        self.battery = None               # dict: voltage, amperage, mah_used
        self.arming_flags = []            # list of flag-name strings
        self.last_update_ts = 0.0         # time.time() of last successful update
        raise NotImplementedError

    def update(self) -> bool:
        """
        Refresh all cached fields from the FC. Update last_update_ts on success.
        Returns True if the read succeeded.
        TODO: call telemetry.read_* and store results.
        """
        raise NotImplementedError

    def age_ms(self) -> float:
        """Milliseconds since the last successful update (for staleness checks)."""
        return (time.time() - self.last_update_ts) * 1000.0

    def has_gps_fix(self) -> bool:
        """True if GPS currently reports a usable fix."""
        raise NotImplementedError
