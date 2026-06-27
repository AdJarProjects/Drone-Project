"""
world/geo.py  --  Translate between maze cells and real-world GPS coordinates.

THE most important glue in the project. The pathfinder thinks in grid cells;
the aircraft lives in GPS lat/lon. This maps between them, given:
    - an origin lat/lon (where cell (0,0) sits in the real world)
    - cell size in meters
    - a heading offset (grid rotation vs. true north)

All bearing/distance math (haversine, destination-point, initial-bearing)
lives here and in brain/guidance.py.
"""

import math


class GeoMapper:
    """Converts maze cells <-> GPS coordinates."""

    def __init__(self, origin_lat: float, origin_lon: float,
                 cell_size_m: float, heading_offset_deg: float = 0.0):
        self.origin_lat = origin_lat
        self.origin_lon = origin_lon
        self.cell_size_m = cell_size_m
        self.heading_offset_deg = heading_offset_deg
        raise NotImplementedError

    def cell_to_gps(self, cell: tuple) -> tuple:
        """
        (row, col) -> (lat, lon) of that cell's center.
        TODO: convert cell offset to meters (north/east), rotate by
        heading_offset, then offset from origin using a destination-point
        formula. Return (lat, lon).
        """
        raise NotImplementedError

    def gps_to_cell(self, lat: float, lon: float) -> tuple:
        """
        (lat, lon) -> nearest (row, col).
        TODO: compute north/east meters from origin (haversine components),
        un-rotate by heading_offset, divide by cell_size, round.
        """
        raise NotImplementedError

    @staticmethod
    def haversine_m(lat1, lon1, lat2, lon2) -> float:
        """Great-circle distance in meters between two GPS points."""
        raise NotImplementedError

    @staticmethod
    def bearing_deg(lat1, lon1, lat2, lon2) -> float:
        """Initial bearing (deg from true north) from point 1 to point 2."""
        raise NotImplementedError
