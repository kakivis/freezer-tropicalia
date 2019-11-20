from Servo import *

LOCK_ANGLE = 90
UNLOCK_ANGLE = 0


class DoorLock:
	def __init__(self, pin):
		self.servo = Servo(pin)

	def lock(self):
		self.servo.set_angle(LOCK_ANGLE)

	def unlock(self):
		self.servo.set_angle(UNLOCK_ANGLE)
