from math import cos, sin, acos, atan, pi
import math
import GreatCircle

def heading_error(initial, final):
    assert initial <= 360
    assert initial >= 0
    assert final <= 360
    assert final >= 0

    diff = final - initial
    absDiff = abs(diff)

    if absDiff <= 180:
        if absDiff == 180:
            return absDiff
        else:
            return diff;
    elif final > initial:
        return absDiff - 360
    else:
        return 360 - absDiff

def heading_difference(a, b):
    result = a - b;
    if result < -180:
        return 360 + result
    if result > 180:
        return 0 - (360 - result)
    return result

def distance(a, b):
     #pk = 180/math.pi;
     lat_a, lon_a = a;
     lat_b, lon_b = b;

     #lat_a /= pk
     #lon_a /= pk
     #lat_b /= pk
     #lon_b /= pk

    # t1 = math.cos(lat_a) * math.cos(lon_a) * math.cos(lat_b) * math.cos(lon_b)
     #t2 = math.cos(lat_a) * math.sin(lon_a) * math.cos(lat_b) * math.sin(lon_b)
     #t3 = math.sin(lat_a) * math.sin(lat_b)
     #tt = math.acos(t1 + t2 + t3)
     #return 6366000 * tt
     return GreatCircle.distance(lat_a,lon_a,lat_b,lon_b)*1000
    

def heading(a, b):
    a_lat, a_lon = a
    b_lat, b_lon = b
    #lat1 = math.radians(a_lat)
    #lat2 = math.radians(b_lat)
    #lon_diff = math.radians(b_lon - a_lon)
    #y = math.sin(lon_diff) * math.cos(lat2)
    #x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1)
    #math.cos(lat2) * math.cos(lon_diff)
    #return (math.degrees(math.atan2(y, x)) + 360) % 360
    return GreatCircle.bearing(a_lat, a_lon, b_lat, b_lon)
    

def move_sail(wind_angle):
    if wind_angle < 180:
        if wind_angle < 70:
            position = 0
        elif wind_angle < 80:
            position = 18
        elif wind_angle < 90:
            position = 36
        elif wind_angle < 110:
            position = 54
        else:
            position = 72
    else:
        if wind_angle >= 290:
            position = 0
        elif wind_angle >= 280:
            position = 18
        elif wind_angle >= 270:
            position = 36
        elif wind_angle >= 250:
            position = 54
        else:
            position = 72;

    return position
