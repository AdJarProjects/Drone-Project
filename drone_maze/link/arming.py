"""
link/arming.py  --  The arm/disarm gate.

Isolated on purpose so the one piece of code that can make motors live is
small and auditable. Arming should go through a dedicated AUX channel
(not stick commands), and this gate refuses to arm while any
arming-disable flag is set.
"""


class ArmGate:
    """Controls and guards the armed state."""

    def __init__(self, connection, control, override_aux_channel: int):
        self.connection = connection
        self.control = control
        self.override_aux_channel = override_aux_channel
        self._armed = False
        raise NotImplementedError

    def can_arm(self, state) -> bool:
        """
        True only if State reports zero arming-disable flags and a GPS fix.
        TODO: check state.arming_flags is empty and state.has_gps_fix().
        """
        raise NotImplementedError

    def arm(self, state) -> bool:
        """
        Arm ONLY if can_arm(state). Returns True if now armed.
        Never force-arm; respect the FC's refusal.
        """
        raise NotImplementedError

    def disarm(self) -> None:
        """Disarm immediately. Always safe to call."""
        raise NotImplementedError

    def is_armed(self) -> bool:
        return self._armed
