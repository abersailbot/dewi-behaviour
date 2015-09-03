from __future__ import print_function
import time
import boat_utils
from boatd_client import Boat

waypoint_error = 10
how_close_to_wind = 45
is_tacking = False
tack_distance = 20
currentSide = 'R'
start_lat = 0
start_lon = 0

HEADING = 0
K_P = 1
K_I = 0.1

integrator = 0

boat = Boat()

def get_rudder_position(heading, wanted_heading):
    current_heading = boat.heading
    print('PID heading:', current_heading, 'wanted:', HEADING, end='')
    error = boat_utils.heading_error(current_heading, HEADING)
    integrator += error
    print('error:', error, 'integrator:', integrator)
    boat.rudder( -(K_P * error + K_I * integrator))

def get_absolute_wind_direction():
    return 10

waypoints = [(-12, 3443), (2, 334)]

for point in waypoints:
    dist_on_left = 0
    dist_on_right = 0
    while boat_utils.distance(boat.position, point) > waypoint_error:
        rudder_position = 0
        absolute_wind_direction = get_absolute_wind_direction()
        desired_heading = boat_utils.heading(boat.postition, point)

        print('position:', boat.position,
            'distance to waypoint:', boat_utils.distance(boat.position, point),
            'bearing to waypoint:', desired_heading)

        if boat_utils.heading_difference(desired_heading, absolute_wind_direction) > how_close_to_wind:
            is_tacking = False
            targetHeading = desired_heading
        else:
            if not is_tacking:
                angle = boat_utils.heading_difference(boat_utils.heading_difference(absolute_wind_direction, how_close_to_wind), desired_heading)
                angle = abs(angle)
                dist_on_left = tack_distance * math.cos(math.radians(angle))
                dist_on_right = tack_distance * math.sin(math.radians(angle))
                # Checking which side is favourable, i.e. closer to the desired heading
                if boat_utils.heading_difference(desired_heading, (absolute_wind_direction + how_close)) < boat_utils.heading_difference(desiredHeading, (absolute_wind_direciton - howClose)):
                    # If right side is favourable
                    current_side = 'R'
                    target_heading = absoulte_wind_direction + how_close
                    if (target_heading > 360):
                        target_heading -= 360
                else:
                    # If left side is favourable
                    current_side = 'L'
                    target_heading = absoulte_wind_direction - how_close
                    if (targetHeading < 0):
                        targetHeading = 360 + target_heading
                start_lat = boat.latitude
                start_long = boat.longitude

                tackingSet = true;
            
            current_distance = boat_utils.distance((start_lat, start_long), (boat.latitude, boat.longitude))
            
            if current_side == 'R':
                target_distance = dist_on_right - current_distance
            else:
                target_distance = dist_on_left - current_distance
 
            # Checking if side should be changed
            if current_side == 'L' and current_distance > dist_on_left:
                # Switching to right side
                current_side = 'R'
                start_lat = boat.latitude
                start_lon = boat.longitude
                target_heading = absolute_wind_direction + how_close
                if target_heading > 360:
                    target_heading -= 360
            elif current_side == 'R' and current_distance > dist_on_right:
                # Switching to left side
                current_side = 'L'
                start_lat = boat.latitude
                start_lon = boat.longitude
                target_heading = absolute_wind_direction - how_close
                if target_heading < 0:
                    target_heading = 360 + target_heading

        # Actually adjusting the rudder
        adjustment = get_rudder_position(boat.heading, desired_heading)
        rudder_position = 180 + adjustment
 
        boat.rudder(rudder_position)
        boat.sail(boat_utils.move_sail(boat.wind - boat.heading))
