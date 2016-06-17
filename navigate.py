from abc import ABCMeta, abstractmethod
import time
import math

import boatdclient
from boatdclient import Bearing

def mirror_angle(angle):
    angle = float(angle)
    if angle > 180:
        return 180 - (angle % 180)
    else:
        return angle

class Navigator(object):
    '''
    Abstract class used to implement behaviours. 

    This should be inherited from and ``check_new_target`` defined to create a
    behaviour with some targets. See ``demo-waypoint-behaviour`` for an example
    of basic waypoint targeting.
    '''
    __metaclass__ = ABCMeta

    def __init__(self, enable_tacking=True):
        self.enable_tacking = enable_tacking

        self.boat = boatdclient.Boat()

        self.target = None
        self.prev_target = None

        self.k_p = 0.6
        self.k_i = 0.003
        self.integrator = 0
        self.integrator_max = 10000

        self.tacking_left = None
        self.tacking_right = None
        self.cone_angle = Bearing(15)
        self.tacking_angle = Bearing(45)
        
        self.cross_track_error = 0

    def set_target(self, value):
        '''Set the target angle for the boat.'''
        self.target = value
        self.integrator = 0

    def update(self):
        '''Update actuators to make progress towards target.'''

        # this currently always assumes that self.target will return a long/lat
        # point

        current_heading = self.boat.heading
        if isinstance(self.target, boatdclient.Point):
            target_heading = self.boat.position.bearing_to(self.target)
        else:
            target_heading = self.target
            
        if isinstance(self.prev_target, boatdclient.Point) and isinstance(self.target, boatdclient.Point):
            # TODO find ideal constant to properly scale up/down effects of cross track error
            self.cross_track_error = self.boat.position.cross_track_distance(self.prev_target, self.target) * 1
        else:
            self.cross_track_error = 0

        # tacking logic
        if target_heading < self.boat.wind.direction + self.tacking_angle and \
           target_heading > self.boat.wind.direction - self.tacking_angle and \
           self.enable_tacking:
            bearing_to_wind = self.boat.position.bearing_to(self.target) - self.boat.wind.direction

            # choose the best initial tack, based on which side of the cone
            # we're on
            if self.tacking_right is None or self.tacking_left is None:
                if bearing_to_wind <= 180:
                    self.tacking_right = True
                    self.tacking_left = False
                else:
                    self.tacking_right = False
                    self.tacking_left = True

            # just between 0 and 180 degrees, needed to reduce if statements as cone is reflected
            modulus_to_wind = mirror_angle(bearing_to_wind)

            # detect if the boat is outside cone
            if modulus_to_wind >= float(self.cone_angle):
                if bearing_to_wind <= 180:
                    target_heading = self.boat.wind.direction + \
                                     self.tacking_angle
                    self.tacking_right = True
                    self.tacking_left = False
                if bearing_to_wind > 180:
                    target_heading = self.boat.wind.direction - \
                                     self.tacking_angle
                    self.tacking_right = False
                    self.tacking_left = True

            # detects if the boat is inside cone
            elif modulus_to_wind < float(self.cone_angle):
                if self.tacking_left is True: 
                    target_heading = self.boat.wind.direction - \
                                     self.tacking_angle
                if self.tacking_right is True:
                    target_heading = self.boat.wind.direction + \
                                     self.tacking_angle
        else:
            self.tacking_left = None
            self.tacking_right = None
        
        error = current_heading.delta(target_heading) + self.cross_track_error
        self.integrator += error
        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max

        print('heading:', current_heading, '	wanted:', target_heading, '	error:',
              error, '	integrator:', self.integrator, '	target:', self.target)
        self.boat.set_rudder( -(self.k_p * error + self.k_i * self.integrator))
        self.update_sail()

    def update_sail(self):
        '''Set the sail to the correct angle based on current wind direction'''

        relative_wind_direction = self.boat.wind.relative_direction

        sail_angle_close_hauled = 0
        sail_angle_close_reach  = 15
        sail_angle_beam_reach   = 25
        sail_angle_broad_reach  = 45
        sail_angle_running      = 70

        if relative_wind_direction < 180:
            if relative_wind_direction < 45:
                sail_angle = sail_angle_close_hauled
            elif relative_wind_direction < 68:
                sail_angle = sail_angle_close_reach
            elif relative_wind_direction < 90:
                sail_angle = sail_angle_beam_reach 
            elif relative_wind_direction < 113:
                sail_angle = sail_angle_broad_reach
            else:
                sail_angle = sail_angle_running
        else:
            if relative_wind_direction >= 315:
                sail_angle = sail_angle_close_hauled
            elif relative_wind_direction >= 292:
                sail_angle = sail_angle_close_reach
            elif relative_wind_direction >= 269:
                sail_angle = sail_angle_beam_reach 
            elif relative_wind_direction >= 246:
                sail_angle = sail_angle_broad_reach
            else:
                sail_angle = sail_angle_running

        self.boat.set_sail(sail_angle)

    def run(self):
        '''
        Run the main loop for the behaviour.
        '''
        while True:
            target = self.check_new_target()
            if target is not None:
                self.prev_target = self.target
                self.set_target(target)

            self.update()

    @abstractmethod
    def check_new_target(self):
        '''
        Check if a new target point needs to be selected.

        Return a new ``Point`` or ``Bearing` if target will be changed,
        ``None`` otherwise.
        '''
        pass
