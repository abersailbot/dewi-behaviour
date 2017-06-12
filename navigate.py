from __future__ import print_function
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

    def __init__(self,
                 enable_tacking=True,
                 enable_cross_track_minimization=True,
                 enable_emergency_maneuver=True):
        self.enable_tacking = enable_tacking
        self.enable_cross_track_minimization = enable_cross_track_minimization
        self.enable_emergency_maneuver = enable_emergency_maneuver

        self.boat = boatdclient.Boat(auto_update=False)

        self.target = None
        self.prev_target = None

        # how long the rudder can be hardover for before trying to snap the boat
        # out of it in an emergency
        self.hardover_rudder_timeout = 20

        # how far over the rudder can be before we assume it's hardover in and emergency
        self.hardover_rudder_threshold = 40

        self.k_p = 0.6
        self.k_i = 0.0
        self.integrator = 0
        self.integrator_max = 200

        # tracks the last time the the rudder was in a good position (i.e. not hard over)
        self.last_time_rudder_not_maxed = time.time()

        self.tacking_left = None
        self.tacking_right = None
        self.cone_angle = Bearing(15)
        self.tacking_angle = Bearing(45)

        self.cross_track_error = 0

    def override_rudder(self, rudder_angle):
        print('override_rudder ing')
        timeout = time.time() + 10
        initial_heading = self.boat.heading

        rudder_angle = -45 if rudder_angle > 0 else 45
        self.boat.set_rudder(rudder_angle)
        while time.time() < timeout and \
                abs(initial_heading.delta(self.boat.heading)) < 170:
            print('override_rudder ong', timeout - time.time())
            time.sleep(0.1)

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

        if self.enable_cross_track_minimization:
            if isinstance(self.prev_target, boatdclient.Point) and isinstance(self.target, boatdclient.Point):
                # TODO find ideal constant to properly scale up/down effects of cross track error
                self.cross_track_error = self.boat.position.cross_track_distance(self.prev_target, self.target) * 5
            else:
                self.cross_track_error = 0

        # tacking logic
        if abs(target_heading.delta(self.boat.wind.absolute)) <=\
           self.tacking_angle and self.enable_tacking:
            bearing_to_wind = self.boat.position.bearing_to(self.target) -\
                              self.boat.wind.absolute

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
                    target_heading = self.boat.wind.absolute + \
                                     self.tacking_angle
                    self.tacking_right = True
                    self.tacking_left = False
                if bearing_to_wind > 180:
                    target_heading = self.boat.wind.absolute - \
                                     self.tacking_angle
                    self.tacking_right = False
                    self.tacking_left = True

            # else the boat is inside cone
            else:
                if self.tacking_left is True:
                    target_heading = self.boat.wind.absolute - \
                                     self.tacking_angle
                if self.tacking_right is True:
                    target_heading = self.boat.wind.absolute + \
                                     self.tacking_angle
        else:
            self.tacking_left = None
            self.tacking_right = None

        # FIXME check if both values are of the correct sign with respect to
        # eachother
        error = current_heading.delta(target_heading) - self.cross_track_error
        self.integrator += error
        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max
        elif self.integrator < -self.integrator_max:
            self.integrator = -self.integrator_max

        rudder_angle = -(self.k_p * error + self.k_i * self.integrator)

        if rudder_angle > 180:
            rudder_angle = 180
        if rudder_angle < -180:
            rudder_angle = -180

        # emergency procedure to get the boat to turn the opposite direction
        # when stuck trying to turn towards a target heading
        if self.enable_emergency_maneuver:
            print('rudder_angle:', rudder_angle, 'hardover_rudder_timeout:', self.hardover_rudder_timeout)
            if abs(rudder_angle) < self.hardover_rudder_threshold:
                self.last_time_rudder_not_maxed = time.time()
            elif time.time() - self.last_time_rudder_not_maxed > self.hardover_rudder_timeout:
                print('time.time(), self.last_time_rudder_not_maxed', time.time(), self.last_time_rudder_not_maxed)
                self.override_rudder(rudder_angle)

                # allow 60 seconds to recover from the maneuver
                self.last_time_rudder_not_maxed = time.time() + 60

        print('heading:', current_heading, '	wanted:', target_heading, '	error:',
              error, '	integrator:', self.integrator, '	target:', self.target, '	rudder_angle:', rudder_angle)
        self.boat.set_rudder(rudder_angle)
        self.update_sail()

    def update_sail(self):
        '''Set the sail to the correct angle based on current wind direction'''

        # not really sure why this 180 needs to exist, but it's a quick bodge
        # to make it work. This should probably be fixed elsewhere at a later
        # date. I suspect boatd/python-boatd has some problems somewhere.
        apparent_wind = self.boat.wind.apparent + 180

        sail_angle_close_hauled = 0
        sail_angle_close_reach  = 10
        sail_angle_beam_reach   = 20
        sail_angle_broad_reach  = 45
        sail_angle_running      = 90

        if apparent_wind < 180:
            if apparent_wind < 45:
                sail_angle = sail_angle_close_hauled
            elif apparent_wind < 68:
                sail_angle = sail_angle_close_reach
            elif apparent_wind < 90:
                sail_angle = sail_angle_beam_reach
            elif apparent_wind < 113:
                sail_angle = sail_angle_broad_reach
            else:
                sail_angle = sail_angle_running
        else:
            if apparent_wind >= 315:
                sail_angle = sail_angle_close_hauled
            elif apparent_wind >= 292:
                sail_angle = sail_angle_close_reach
            elif apparent_wind >= 269:
                sail_angle = sail_angle_beam_reach
            elif apparent_wind >= 246:
                sail_angle = sail_angle_broad_reach
            else:
                sail_angle = sail_angle_running

        self.boat.set_sail(sail_angle)

    def run(self):
        '''
        Run the main loop for the behaviour.
        '''
        while True:
            time1 = time.time()

            self.boat.update()
            target = self.check_new_target()
            if target is not None:
                self.prev_target = self.target
                self.set_target(target)

            self.update()

            # FIXME: remove this timing information after
            # https://github.com/boatd/boatd/issues/68 is somewhat completed
            time2 = time.time()
            with open('timing', 'a') as f:
                f.write('{}\n'.format(time2-time1))

    @abstractmethod
    def check_new_target(self):
        '''
        Check if a new target point needs to be selected.

        Return a new ``Point`` or ``Bearing` if target will be changed,
        ``None`` otherwise.
        '''
        pass
