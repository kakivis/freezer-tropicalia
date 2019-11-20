from Modules.Cryptography.Crypt import AsymmetricCryptography
from Modules.Lock.DoorLock import DoorLock
from Modules.EventLogger.EventLogger import EventLogger


class TropicaliaFreezer:
	def __init__(self):
		self.crypt = AsymmetricCryptography()
		# self.door_locker = DoorLock(23)


if __name__ == '__main__':
	print "olá"
