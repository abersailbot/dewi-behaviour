import time
import boat_utils
from boatd_client import Boat

HEADING = 200
K_P = 1
K_I = 0.1

integrator = 0

boat = Boat()

while True:
    current_heading = boat.heading
    print 'heading:', current_heading, 'wanted:', HEADING,
    error = boat_utils.heading_error(current_heading, HEADING)
    integrator += error
    print  'error:', error, 'integrator:', integrator
    boat.rudder( -(K_P * error + K_I * integrator))
    time.sleep(0.5)
