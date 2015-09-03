from __future__ import print_function
import time
import boat_utils
from boatd_client import Boat

waypoint_error = 10

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

waypoints = [(-12, 3443), (2, 334)]

for point in waypoints:
    while boat_utils.distance(boat.position, point) > waypoint_error:
        print('position:', boat.position,
            'distance to waypoint:', boat_utils.distance(boat.position, point),
            'bearing to waypoint:', boat_utils.heading(boat.position, point))

        boat.rudder(
            get_rudder_position(boat.heading,
            boat_utils.heading(boat.position, point))
            )
        boat.sail(boat_utils.move_sail(boat.wind - boat.heading))
