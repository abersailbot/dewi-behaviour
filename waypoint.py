from point import Point

class Waypoints(object):
    def __init__(self, gps, points=None):
        self._points = points if points is not None else []
        self._currentWaypoint = 0
        self._gps = gps

    def add_point(self, point):
        """Add a waypoint to the end of the current list of waypoints"""
        self._points += [point]

    @property
    def current(self):
        """Return the next waypoint"""
        return self._points[self._currentWaypoint]

    def get_waypoint(self, n):
        """Return the waypoint n places along the path"""
        return self._points[n]

    def distance(self):
        """Return the distance to the next waypoint in meters"""
        return self._gps.position.distance_to(self.next)

    def bearing(self):
        """Return the bearing to the nextwaypoint"""
        return self._gps.position.bearing_to(self.next)

    def set_next(self):
        """Assign the next waypoint to the subsequent point in the list"""
        self._currentWaypoint = min(self._currentWaypoint + 1,
                                    len(self._points) - 1)
    
    @property
    def next(self):
        """Return the next waypoint"""
        return self._points[self._currentWaypoint + 1]

    def set_path(self, path):
        """Replace the current set of waypoints with a new path"""
        self._points = path

    @property
    def waypointNumber(self):
        """Return the number of the current target waypoint"""
        return self._currentWaypoint

    def load_from_file(self, filename):
        with open(filename) as f:
            lines = f.readlines()
        for line in lines:
            self.add_point(Point(*map(float, line.split())))

if __name__ == '__main__':
    w = Waypoints()
    w.load_from_file('waypoints.pnts')
