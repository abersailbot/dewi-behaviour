from __future__ import print_function
import time
import math
import boat_utils
from boatd_client import Boat


#waypoints = [(60.1050, 19.9500), (60.1050, 19.9560), (60.1080, 19.9560), (60.1080, 19.9500), (60.1050, 19.9500), (60.105461, 19.946920)]
waypoints = [(60.106065, 19.947596), (60.105589, 19.948669), (60.105536, 19.947103)]

waypoint_error = 10
how_close_to_wind = 45
is_tacking = False
tack_distance = 20
current_side = 'R'
start = (0, 0)
fake_wind_direction = 200


dist_on_left = 0
dist_on_right = 0

K_P = 1.25
K_I = 0.009

integrator = 0
integrator_max = 1000

boat = Boat()

def get_rudder_position(heading, wanted_heading):
    global integrator

    current_heading = boat.heading
    print('PID heading:', current_heading, 'wanted:', wanted_heading, end='')
    error = boat_utils.heading_error(current_heading, wanted_heading)
    
    integrator += error
    integrator = integrator * 0.99
    
    if integrator > integrator_max:
	integrator = integrator_max

    if integrator < -integrator_max:
	integrator = -integrator_max

    print(' error:', error, 'integrator:', integrator)
    boat.rudder( -(K_P * error + K_I * integrator))

def get_absolute_wind_direction():
    return fake_wind_direction

def calculate_tack(desired_heading, target_heading, absolute_wind_direction):
    global is_tacking

    if not is_tacking:
        angle = boat_utils.heading_difference(boat_utils.heading_difference(absolute_wind_direction, how_close_to_wind), desired_heading)
        angle = abs(angle)
        dist_on_left = tack_distance * math.cos(math.radians(angle))
        dist_on_right = tack_distance * math.sin(math.radians(angle))
        
        # Checking which side is favourable, i.e. closer to the desired heading
        left_temp = absolute_wind_direction + how_close_to_wind
        if left_temp > 360:
            left_temp -= 360
        right_temp = absolute_wind_direction - how_close_to_wind
        if right_temp < 0:
            right_temp += 360
        if boat_utils.heading_difference(desired_heading, left_temp) < boat_utils.heading_difference(desired_heading, right_temp):
            # If right side is favourable
            current_side = 'R'
            target_heading = absolute_wind_direction + how_close_to_wind
            if (target_heading > 360):
                target_heading -= 360
        else:
            # If left side is favourable
            current_side = 'L'
            target_heading = absoulte_wind_direction - how_close_to_wind
            if (target_heading < 0):
                target_heading = 360 + target_heading
        start = boat.position

        is_tacking = True;
    
    current_distance = boat_utils.distance(start, boat.position)
    
    if current_side == 'R':
        target_distance = dist_on_right - current_distance
    else:
        target_distance = dist_on_left - current_distance

    # Checking if side should be changed
    if current_side == 'L' and current_distance > dist_on_left:
        # Switching to right side
        current_side = 'R'
        start = boat.position
        target_heading = absolute_wind_direction + how_close_to_wind
        if target_heading > 360:
            target_heading -= 360
    elif current_side == 'R' and current_distance > dist_on_right:
        # Switching to left side
        current_side = 'L'
        start = boat.position
        target_heading = absolute_wind_direction - how_close_to_wind
        if target_heading < 0:
            target_heading = 360 + target_heading
    return target_heading

print("starting")

for point in waypoints:
    while boat_utils.distance(boat.position, point) > waypoint_error:
	
        rudder_position = 0
        absolute_wind_direction = get_absolute_wind_direction()
        desired_heading = boat_utils.heading(boat.position, point)
	target_heading = 0
    
        if abs(boat_utils.heading_difference(desired_heading, absolute_wind_direction)) > how_close_to_wind:
            is_tacking = False
            target_heading = desired_heading
	    #print('target_heading in if statement',target_heading)
        else:
	    is_tacking = False
	    print("calculating tacking")
            #target_heading = calculate_tack(desired_heading, target_heading, absolute_wind_direction)


        # Actually adjusting the rudder
        get_rudder_position(boat.heading, target_heading)
 
        #boat.rudder(rudder_position)
	relative_wind = boat_utils.heading_difference(get_absolute_wind_direction(),boat.heading)

	#make relative wind 0-360
	if relative_wind < 0:
	    relative_wind = relative_wind + 360 

        print('position:', boat.position,
            'waypoint:',point,
            'distance to waypoint:', boat_utils.distance(boat.position, point),
            'desired_heading:', desired_heading,
            'target_heading:', target_heading,
            'is_tacking:', is_tacking,
            'relative_wind:', relative_wind)

 

	boat.sail(boat_utils.move_sail(relative_wind))
	print("")

