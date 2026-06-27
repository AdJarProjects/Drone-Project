"""
brain/guidance.py  --  Turn "where am I + where next" into a movement command.

Given the current State and the target waypoint's GPS, compute the heading
and a normalized roll/pitch/yaw/throttle command to drive toward it. This
is GUIDANCE only -- INAV's onboard gyro loop handles STABILIZATION. Do not
try to do attitude stabilization from here; the MSP link is far too slow.
"""


def compute_guidance(state, target_gps: tuple, geo, config: dict) -> dict:
    """
    Return a command dict: {'roll', 'pitch', 'throttle', 'yaw'} as
    normalized values for link/control.py.

    TODO:
      1. bearing = geo.bearing_deg(current -> target)
      2. error   = shortest angular diff between bearing and current yaw
      3. yaw cmd = turn toward target (proportional to error)
      4. pitch   = forward at cruise_speed once roughly aligned
      5. throttle= altitude-hold toward target_altitude_m
      6. clamp everything to limits.max_tilt
    Keep it simple first (point-then-go); refine later.
    """
    raise NotImplementedError


def angle_diff_deg(a: float, b: float) -> float:
    """Smallest signed difference a-b wrapped to [-180, 180]."""
    raise NotImplementedError
