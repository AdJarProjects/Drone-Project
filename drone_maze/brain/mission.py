"""
brain/mission.py  --  Walks the waypoint list one cell at a time.

The bridge between the abstract path and real movement. Holds the planned
waypoints, tracks which one we're heading to, and advances when the
aircraft gets within waypoint_radius of the current target.
"""


class Mission:
    """Sequences the aircraft through the planned path."""

    def __init__(self, waypoints: list, geo, waypoint_radius_m: float):
        """
        waypoints: list of (row, col) cells from find_path.
        geo:       GeoMapper, to convert target cells to GPS.
        """
        self.waypoints = waypoints
        self.geo = geo
        self.waypoint_radius_m = waypoint_radius_m
        self.index = 0
        raise NotImplementedError

    def current_target(self) -> tuple:
        """
        Return the GPS (lat, lon) of the current target waypoint,
        or None if the mission is complete.
        """
        raise NotImplementedError

    def reached(self, current_lat: float, current_lon: float) -> bool:
        """
        True if within waypoint_radius_m of the current target.
        TODO: use geo.haversine_m to the current target's GPS.
        """
        raise NotImplementedError

    def advance(self) -> None:
        """Move to the next waypoint."""
        self.index += 1

    def is_complete(self) -> bool:
        """True once all waypoints are consumed."""
        return self.index >= len(self.waypoints)

    def replan(self, new_waypoints: list) -> None:
        """
        Swap in a freshly planned path (e.g. after a live maze edit),
        resetting progress sensibly.
        """
        raise NotImplementedError
