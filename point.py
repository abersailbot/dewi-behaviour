import math
from math import sin as sin
from math import cos as cos

from bearing import Bearing

EARTH_RADIUS = 6371009 #in meters

class Point(object):
    """A point on the face of the earth"""
    def __init__(self, latitude, longitude):
        self._lat = latitude
        self._long = longitude

    @classmethod
    def from_radians(cls, lat_radians, long_radians):
        """Return a new instance of Point from a pair of coordinates in radians"""
        return cls(math.degrees(lat_radians), math.degrees(long_radians))

    def __getitem__(self, key):
        if key == 0:
            return self._lat
        elif key == 1:
            return self._long
        else:
            raise IndexError('Point objects can only have two coordinates')

    def __iter__(self):
        """Return an iterator containing the lat and long"""
        return iter([self.lat, self.long])

    def __str__(self):
        """Return a string representation of the point"""
        return '{0:0.2f}N, {1:0.2f}W'.format(*list(self))

    @property
    def lat(self):
        """Return the latitude in degrees"""
        return self._lat

    @property
    def long(self):
        """Return the longitude in degrees"""
        return self._long

    @property
    def lat_radians(self):
        """Return the latitude in radians"""
        return math.radians(self.lat)

    @property
    def long_radians(self):
        """Return the longitude in radians"""
        return math.radians(self.long)

    def distance_to(self, point):
        """Return the distance between two points in meters"""
        angle = math.acos(
                sin(self.lat_radians) * sin(point.lat_radians) +
                cos(self.lat_radians) * cos(point.lat_radians) *
                cos(self.long_radians - point.long_radians)
            )
        return angle * EARTH_RADIUS

    def bearing_to(self, point):
        """Return the bearing to another point"""
        delta_long = point.long_radians - self.long_radians
        y = sin(delta_long) * cos(point.lat_radians)
        x = (
             cos(self.lat_radians) * sin(point.lat_radians) -
             sin(self.lat_radians) * cos(point.lat_radians) * cos(delta_long)
            )
        radians = math.atan2(y, x)
        return Bearing.from_radians(radians)

#do a couple of tests
if __name__ == '__main__':
    castle = Point(52.41389, -4.09098) #aber castle
    print castle
    hill = Point(52.42459, -4.08339) #Constitution hill
    print hill

    #distance should be ~1.29844 km
    print castle.distance_to(hill)
    print castle.bearing_to(hill)
    
    # should be ~90 degrees
    print Point(52.41398, -4.4627).bearing_to(Point(52.41398, -4.09122))
