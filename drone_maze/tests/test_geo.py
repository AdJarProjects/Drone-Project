"""
tests/test_geo.py  --  Validate cell <-> GPS conversions. Laptop only.

The geo math is easy to get subtly wrong (rotation sign, lat/lon order,
meters-per-degree). These tests catch that before it sends the aircraft
the wrong way.
"""

# from world.geo import GeoMapper


def test_round_trip():
    """
    cell_to_gps then gps_to_cell should return the original cell for a
    spread of cells. TODO.
    """
    raise NotImplementedError


def test_origin_maps_to_origin():
    """Cell (0,0) center should be ~ the configured origin lat/lon. TODO."""
    raise NotImplementedError


def test_known_distance():
    """
    Two cells N apart should be ~ N * cell_size_m via haversine_m.
    Confirms scale is right. TODO.
    """
    raise NotImplementedError


if __name__ == "__main__":
    test_round_trip()
    test_origin_maps_to_origin()
    test_known_distance()
    print("All geo tests passed.")
