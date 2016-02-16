# Dewi - Waypoint Navigation - Aber SailBot
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

dewi = Boat()

# Function to sail to each waypoint (calling functions to navigate to each)
def sail():
	# Loop for all waypoint tuples in the waypoints array
	for waypoint_count in waypoints:
		