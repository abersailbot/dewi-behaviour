# Dewi - Waypoint Navigation - AberSailbot
# =========================================

import math
import boat_utils
from boatd_client import Boat

# All the waypoints can be added to this list of tuples
waypoints = [(52.406988,-4.090990)] 

# Use this waypoint for Dewi to return to after completing the course
home_waypoint = (52.406988,-4.090990) 

# The number of laps of the course to complete before returning home
laps = 1

# The GPS Error in Metres
gps_error = 10

dewi = Boat()

# Function to sail to each waypoint (calling functions to navigate to each)
def sail():
	# Loop for all waypoint tuples in the waypoints array
	for waypoint in waypoints:
		# Navigate to the next waypoint
		navigate(waypoint)
	# Once all the waypoints have been visited, the boat sails back to the home waypoint
	navigate(home_waypoint)
	
# Function to navigate to the next waypoint
def navigate(waypoint):
	# Variable to hold the boolean value of whether the waypoint has been reached or not
	waypoint_reached = false
	# Repeat while the waypoint has not been reached
	while waypoint_reached == false :
		# Check whether the waypoint has been reached and whether we should move on to the next waypoint
		waypoint_reached = check_waypoint_reached(waypoint);
		
def check_waypoint_reached(waypoint):
	# Check proximity to the waypoint to decide if it has been reached - we can change the specification of this e.g. if we need to navigate around buoys when needed
	if boat_utils.distance(dewi.position, waypoint) > gps_error:
		return true
	else:
		return false