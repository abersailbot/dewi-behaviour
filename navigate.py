from abc import ABCMeta, abstractmethod
import time

import boatdclient


class Navigator(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.boat = boatdclient.Boat(convenience=True)

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
        '''Update actuators to make progress towards targets.'''
        current_heading = self.boat.heading
        if isinstance(self.target, boatdclient.Point):
            target_heading = self.boat.position.bearing_to(self.target)
        else:
            target_heading = self.target

        error = current_heading.delta(target_heading)
        self.integrator += error
        if self.integrator > self.integrator_max:
            self.integrator = self.integrator_max

        print('heading:', current_heading, '	wanted:', target_heading, '	error:',
              error, '	integrator:', self.integrator, '	target:', self.target)
        self.boat.set_rudder( -(self.k_p * error + self.k_i * self.integrator))

    def run(self):
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

        Return a new ``Point`` if target will be changed, None otherwise.
        '''
        pass
