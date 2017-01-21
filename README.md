# gps_2_road
Project gps data points to the nearest road

These scripts was created in order to project GPS points from my bike rides onto the nearest road.  It does this by projecting the GPS point to the nearest point on the surrounding roads using shapely.  The point is then assigned to the projected point on the vincenty distance minimizing road.
