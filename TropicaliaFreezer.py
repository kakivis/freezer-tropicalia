from Modules.Cryptography.Crypt import AsymmetricCryptography
from Modules.Lock.DoorLock import DoorLock
from Modules.EventLogger.EventLogger import EventLogger
from Modules.BleManager import BleManager
from Modules.StorageManager import StorageManager
from datetime import date


class TropicaliaFreezer:
	def __init__(self):
		self.crypt = AsymmetricCryptography()
		# self.lock_handler = DoorLock(23)
		# self.storage_handler = StorageManager()
		self.ble_service = BleManager()
		self.event_logger = EventLogger('log_' + date.today().strftime("%d_%m_%y"))


if __name__ == '__main__':
	tropicalia_freezer = TropicaliaFreezer()
	tropicalia_freezer.ble_service.run()
