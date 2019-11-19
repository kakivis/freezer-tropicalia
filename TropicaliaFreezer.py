from modules.cryptography.Crypt import AsymmetricCryptography
from modules.door_locks.DoorLock import DoorLock
from modules.event_logger.EventLogger import EventLogger


class TropicaliaFreezer:
	def __init__(self):
		self.crypt = AsymmetricCryptography()
		# self.door_locker = DoorLock(23)


if __name__ == '__main__':
	print "olá"
