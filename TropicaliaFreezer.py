#from modules.bt.bluetooth_driver import *
from modules.cryptography.AsymmetricCryptography import AsymmetricCryptography
from modules.door_locks.door_lock import DoorLock
from modules.event_logger.event_logger import EventLogger


class TropicaliaFreezer:
	def __init__(self):
		self.crypt = AsymmetricCryptography()
		# self.door_locker = DoorLock(23)


if __name__ == '__main__':
	print "olá"
