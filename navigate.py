from abc import ABCMeta, abstractmethod
import time

import boatdclient


class Navigator(object):
    '''
    Abstract class used to implement behaviours. 

    This should be inherited from and ``check_new_target`` defined to create a
    behaviour with some targets. See ``demo-waypoint-behaviour`` for an example
    of basic waypoint targeting.
    '''
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
        '''Update actuators to make progress towards target.'''
        current_heading = self.boat.heading
        if isinstance(self.target, boatdclient.Point):
            target_heading = self.boat.position.bearing_to(self.target)
        else:
            target_heading = self.target

#Tacking logic
	if target_heading < self.boat.wind_direction + Bearing(45) and target_heading > self.boat.wind_direction - Bearing(45):

	    if self.boat.position.bearing_to(self.target) > 10:
	        target_heading = self.boat.wind_direction + Bearing(45)

	    elif self.boat.position.bearing_to(self.target) < 10:
	        target_heading = self.boat.wind_direction - Bearing(45)

	    elif current_heading < self.boat.wind_direction:
                target_heading = self.boat.wind_direction - Bearing(45)

            else:
		target_heading = self.boat.wind_direction + Bearing(45)



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

	relative_wind_direction = self.boat.wind_direction - Bearing(self.boat.heading)
	if relative_wind_direction < 180:
			if relative_wind_direction < 70:
				newSailAngle = 0
			elif relative_wind_direction < 80:
				newSailAngle = 18
			elif relative_wind_direction < 90:
				newSailAngle = 36
			elif relative_wind_direction < 110:
				newSailAngle = 54
			else:
				newSailAngle = 72
		else:
			if relative_wind_direction >= 290:
				newSailAngle = 0
			elif relative_wind_direction >= 280:
				newSailAngle = 342
			elif relative_wind_direction >= 270:
				newSailAngle = 324
			elif relative_wind_direction >= 250:
				newSailAngle = 306
			else:
				newSailAngle = 288
				
		self.boat.set_sail(newSailAngle)

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
