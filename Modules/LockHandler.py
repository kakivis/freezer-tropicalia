from Lock.DoorLock import DoorLock

PIN_INSIDE_LOCK = 15   # Place Holder
PIN_OUTSIDE_LOCK = 16  # Place Holder


class LockHandler:
	def __init__(self):
		self.inside_lock = DoorLock(PIN_INSIDE_LOCK)
		self.outside_lock = DoorLock(PIN_OUTSIDE_LOCK)

	def unlock(self):
		self.inside_lock.unlock()
		self.outside_lock.unlock()

	def lock(self):
		self.inside_lock.lock()
		self.outside_lock.lock()

