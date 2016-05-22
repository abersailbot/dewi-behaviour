from abc import ABCMeta, abstractmethod

import boatdclient


class Navigator(object):
    __metaclass__ = ABCMeta

    def __init__(self):
        self.boat = boatdclient.Boat(convenience=True)

        self.target_point = None

    def set_target_heading(self, angle):
        '''Set the target angle for the boat.'''
        pass

    def update(self):
        '''Update actuators to make progress towards targets.'''
        pass

    def check_new_target(self):
        '''
        Check if a new target point needs to be selected.

        Return a new ``Point`` if target will be changed, None otherwise.
        '''
        pass
