"""
link/control.py  --  Convert high-level intent into MSP RC-override commands.

This is the ONLY module that sends movement commands. It takes a guidance
command (desired roll/pitch/yaw/throttle as normalized values) and maps it
to RC channel microsecond values (1000-2000) in INAV's AETR order, then
pushes them via MSP_SET_RAW_RC.

SAFETY:
  - Requires MSP RX enabled in INAV (Receiver tab) and MSP RC Override.
  - Never sends until ArmGate confirms armed-and-authorized.
  - handoff() must instantly return control to the transmitter.
  - Test PROPS OFF until arm/disarm and failsafe are fully verified.
"""


# Channel order INAV expects by default: Roll, Pitch, Throttle, Yaw, then AUX.
AETR_ORDER = ("roll", "pitch", "throttle", "yaw")


class Control:
    """Sends RC-override commands to the FC."""

    def __init__(self, connection, limits: dict):
        """Keep the Connection and the safety limits (max_tilt, etc.)."""
        self.connection = connection
        self.limits = limits
        raise NotImplementedError

    def _normalized_to_pwm(self, value: float) -> int:
        """
        Map a normalized command (-1..1, or 0..1 for throttle) to a
        1000-2000us RC value. Apply limit clamps here.
        """
        raise NotImplementedError

    def send(self, cmd: dict) -> bool:
        """
        cmd = {'roll', 'pitch', 'throttle', 'yaw', optionally aux...}.
        Convert to PWM, assemble channel list in AETR order, send via
        MSP_SET_RAW_RC. Returns True on success.
        """
        raise NotImplementedError

    def hold(self) -> None:
        """Send a neutral/hover command (level, holding altitude)."""
        raise NotImplementedError

    def handoff(self) -> None:
        """
        Relinquish MSP override so the transmitter regains control.
        Called by failsafe. Must be safe to call repeatedly.
        """
        raise NotImplementedError
