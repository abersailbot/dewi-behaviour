import math

class Bearing(object):
    """An angle between 0 and 360 degrees"""
    def __init__(self, degrees):
        self._degrees = float(degrees % 360)

    @classmethod
    def from_radians(cls, radians):
        return cls(math.degrees(radians))

    @property
    def degrees(self):
        return self._degrees

    def __float__(self):
        return self._degrees

    def __add__(self, n):
        return Bearing(float(self) + float(n))

    def __radd__(self, n):
        return Bearing(float(self) + float(n))

    def __sub__(self, n):
        return Bearing(float(self) - float(n))

    def __rsub__(self, n):
        return Bearing(float(n) - float(self))

    def __str__(self):
        return '{0:0.2f} degrees clockwise from north'.format(self.degrees)

    def __int__(self):
        return int(self._degrees)
