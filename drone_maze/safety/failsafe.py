"""
safety/failsafe.py  --  Watchdog. Non-negotiable for autonomous flight.

Checked every loop BEFORE any movement command. Watches for the conditions
that should abort autonomy and hand control back to the pilot:
    - GPS fix lost
    - battery below min_battery_v
    - telemetry stale (link lag/loss) beyond max_stale_ms
    - manual-override switch flipped on the transmitter
    - loop stalls

On any trigger, main.py must call Control.handoff() so the transmitter
takes over immediately.
"""


class FailsafeStatus:
    """Result of a failsafe check."""
    def __init__(self, safe: bool, reason: str = ""):
        self.safe = safe
        self.reason = reason


class Failsafe:
    """Evaluates whether it's safe to continue autonomous control."""

    def __init__(self, config: dict):
        self.min_battery_v = config["limits"]["min_battery_v"]
        self.max_stale_ms = config["limits"]["max_stale_ms"]
        self.override_aux = config["safety"]["override_aux_channel"]
        raise NotImplementedError

    def check(self, state) -> FailsafeStatus:
        """
        Run all checks against the current State.
        Return FailsafeStatus(safe=False, reason=...) on the FIRST failure,
        else FailsafeStatus(safe=True).
        TODO:
          - state.has_gps_fix()
          - state.battery['voltage'] >= min_battery_v
          - state.age_ms() <= max_stale_ms
          - manual override channel not active
        """
        raise NotImplementedError

    def manual_override_active(self, state) -> bool:
        """True if the pilot has flipped the override switch (AUX channel high)."""
        raise NotImplementedError
