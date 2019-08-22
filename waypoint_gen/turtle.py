#!/usr/bin/env python
import sys
import math

def projectPoint(bearing,dist,lat1,lon1):
    '''projects a point on a given bearing, for a given distance from a latitude and longitude
    latitude and longitude and beading are in degrees. Distance is in kilometres'''
    dist = dist/6367000  # d = angular distance covered on earth's surface
    #convert to radians
    bearing = bearing * (math.pi / 180)

    lat1 = lat1 * (math.pi/180)
    lon1 = lon1 * (math.pi/180)
    lat2 = math.asin( math.sin(lat1)*math.cos(dist) + math.cos(lat1)*math.sin(dist)*math.cos(bearing) )
    lon2 = lon1 + math.atan2(math.sin(bearing)*math.sin(dist)*math.cos(lat1), math.cos(dist)-math.sin(lat1)*math.sin(lat2))

    if math.isnan(lat2) or math.isnan(lon2):
        print("isnan in project point")
        sys.exit(1)

    #convert back to degrees
    lat2 = lat2 * (180/math.pi)
    lon2 = lon2 * (180/math.pi)
    return (lat2,lon2)

class Turtle:
    def __init__(self,lat,lon):
        self.lat=lat
        self.lon=lon
        self.angle=0.0

    def left(self,angle):
        self.angle = self.angle-angle
        if self.angle<0:
            self.angle = self.angle + 360

    def right(self,angle):
        self.angle = self.angle+angle
        if self.angle>360:
            self.angle = self.angle - 360

    def forward(self,dist):
        self.lat,self.lon = projectPoint(self.angle,float(dist),self.lat,self.lon)

    def dist(self,d):
        self.dist=d

    def print(self):
        print("%f %f" % (self.lat,self.lon))
