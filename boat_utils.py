from math import cos, sin, acos, pi

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
     pk = 180/math.pi;
     lat_a, lon_a = a;
     lat_b, lon_b = b;

     lat_a /= pk
     lon_a /= pk
     lat_b /= pk
     lon_b /= pk

     t1 = cos(lat_a) * cos(lon_a) * cos(lat_b) * cos(lon_b)
     t2 = cos(lat_a) * sin(lon_a) * cos(lat_b) * sin(lon_b)
     t3 = sin(lat_a) * sin(lat_b)
     tt = acos(t1 + t2 + t3)
     return 6366000 * tt
