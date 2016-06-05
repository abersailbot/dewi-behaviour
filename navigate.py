from abc import ABCMeta, abstractmethod
import time

import boatdclient
from boatdclient import Bearing


class Navigator(object):
    '''
    Abstract class used to implement behaviours. 

    This should be inherited from and ``check_new_target`` defined to create a
    behaviour with some targets. See ``demo-waypoint-behaviour`` for an example
    of basic waypoint targeting.
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        self.boat = boatdclient.Boat()

        self.target = None

        self.k_p = 0.6
        self.k_i = 0.003
        self.integrator = 0
        self.integrator_max = 10000

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

        # tacking logic
        if target_heading < self.boat.wind.direction + Bearing(45) and target_heading > self.boat.wind.direction - Bearing(45):

            # FIXME: make relative to wind angle
            
            # FIXME: Wrap around at 180 deg instead of 360 - the logic needn't take into account what side of the wind it is on. Only, e.g. 45 degrees off the wind etc.
            

            cone_angle = 15

            bearing_to_wind = self.boat.position.bearing_to(self.target) - self.boat.wind.direction
            print 'I am tacking and bearing_to_wind is', bearing_to_wind
            if self.boat.relative_wind > 180:
                pass

			# Detects if it is outside the cone
            if bearing_to_wind > cone_angle and bearing_to_wind > (360 - cone_angle):
                if bearing_to_wind <= 180:
                    target_heading = self.boat.wind.direction - Bearing(45)
                if bearing_to_wind > 180:
                    target_heading = self.boat.wind.direction + Bearing(45)

			# Detects if it is inside cone
            elif bearing_to_wind < cone_angle and bearing_to_wind < (360 - cone_angle):
                if bearing_to_wind <= 180:      
                    target_heading = self.boat.wind.direction - Bearing(45)
                if bearing_to_wind > 180:
                    target_heading = self.boat.wind.direction + Bearing(45)

        error = current_heading.delta(target_heading)
        self.integrator += error
        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max

        print('heading:', current_heading, '	wanted:', target_heading, '	error:',
              error, '	integrator:', self.integrator, '	target:', self.target)
        self.boat.set_rudder( -(self.k_p * error + self.k_i * self.integrator))
        self.update_sail()

    def update_sail(self):
        '''Set the sail to the correct angle based on current wind direction'''

        relative_wind_direction = self.boat.wind.direction - self.boat.heading

        if relative_wind_direction < 180:
            if relative_wind_direction < 70:
                sail_angle = 0
            elif relative_wind_direction < 80:
                sail_angle = 18
            elif relative_wind_direction < 90:
                sail_angle = 36
            elif relative_wind_direction < 110:
                sail_angle = 54
            else:
                sail_angle = 72
        else:
            if relative_wind_direction >= 290:
                sail_angle = 0
            elif relative_wind_direction >= 280:
                sail_angle = 342
            elif relative_wind_direction >= 270:
                sail_angle = 324
            elif relative_wind_direction >= 250:
                sail_angle = 306
            else:
                sail_angle = 288

        self.boat.set_sail(sail_angle)

    def run(self):
        '''
        Run the main loop for the behaviour.
        '''
        while True:
            target = self.check_new_target()
            if target is not None:
                self.set_target(target)

            self.update()
            time.sleep(0.1)

    @abstractmethod
    def check_new_target(self):
        '''
        Check if a new target point needs to be selected.

        Return a new ``Point`` or ``Bearing` if target will be changed,
        ``None`` otherwise.
        '''
        pass
