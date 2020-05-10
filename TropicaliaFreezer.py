import json
import dbus
import dbus.mainloop.glib
from Modules.Cryptography.Crypt import AsymmetricCryptography
from Modules.Lock.DoorLock import DoorLock
from Modules.EventLogger.EventLogger import EventLogger
from Modules.StorageManager import StorageManager
from Modules.Bluetooth.BluetoothDriver import *
from datetime import date
from gi.repository import GObject
import RPi.GPIO as GPIO

GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'
TROPICALIA_SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0'
CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1'
LOCAL_NAME = 'TropilaciaFreezer'


class TropicaliaCharacteristic(Characteristic):
	def __init__(self, bus, index, service):
		Characteristic.__init__(
			self, bus, index,
			CHARACTERISTIC_UUID,
			['secure-read', 'secure-write'],
			service)
		self.value = []

	@staticmethod
	def parse_instruction_bytes(value):
		return ''.join([str(v) for v in value])

	def ReadValue(self, options):
		print('ReadValue: ' + self.parse_intruction_bytes(self.value))
		return self.value

	def WriteValue(self, value, options):
		print('WriteValue b4: ' + ''.join([str(v) for v in self.value]))
		instruction = self.parse_instruction_bytes(value)
		tropicalia_freezer.handle_instruction(instruction)
		print('WriteValue after: ' + ''.join([str(v) for v in self.value]))

		self.value = value


class TropicaliaService(Service):
	def __init__(self, bus, index):
		Service.__init__(self, bus, index, TROPICALIA_SERVICE_UUID, True)
		self.add_characteristic(TropicaliaCharacteristic(bus, 0, self))


class TropicaliaApplication(Application):
	def __init__(self, bus):
		Application.__init__(self, bus)
		self.add_service(TropicaliaService(bus, 0))


class TropicaliaAdvertisement(Advertisement):
	def __init__(self, bus, index):
		Advertisement.__init__(self, bus, index, 'peripheral')
		self.add_service_uuid(TROPICALIA_SERVICE_UUID)
		self.add_local_name(LOCAL_NAME)
		self.include_tx_power = True


class TropicaliaFreezer:
	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		self.crypt = AsymmetricCryptography()
		self.lock_handler = DoorLock(16)
		self.storage_handler = StorageManager()
		self.event_logger = EventLogger('log_' + date.today().strftime("%d_%m_%y"))
		self.app = None
		self.adv = None
		self.mainloop = None
		self.initialize_ble()

	def initialize_ble(self):
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		bus = dbus.SystemBus()
		adapter = find_adapter(bus)
		if not adapter:
			raise Exception('BLE adapter not found')
		service_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter), GATT_MANAGER_IFACE)
		ad_manager = dbus.Interface(bus.get_object(BLUEZ_SERVICE_NAME, adapter), LE_ADVERTISING_MANAGER_IFACE)
		self.app = TropicaliaApplication(bus)
		self.adv = TropicaliaAdvertisement(bus, 0)
		self.mainloop = GObject.MainLoop()
		service_manager.RegisterApplication(self.app.get_path(), {},
			reply_handler=register_app_cb,
			error_handler=register_app_error_cb)
		ad_manager.RegisterAdvertisement(self.adv.get_path(), {},
			reply_handler=register_ad_cb,
			error_handler=register_ad_error_cb)

	def handle_instruction(self, instruction):
		instructions = ['consult_stock', 'get_last_events', 'unlock_freezer', 'lock_freezer', 'test_cryptography']
		if instruction not in instructions:
			print 'There is no such instruction, please check the whitelisted instructions.'
			return
		method = getattr(self, instruction, lambda: 'Invalid')
		return method()

	def consult_stock(self):
		print 'consult_stock NOT IMPLEMENTED YET'

	def get_last_events(self):
		events = self.event_logger.get_events_from_file()
		events_as_string = json.dumps(events)
		services = self.app.get_services()
		print "found services " + str(len(services))
		service = services[-1]
		print service.get_properties()
		characteristics = service.get_characteristics()
		print "found characteristics " + str(len(characteristics))
		characteristic = characteristics[-1]
		characteristic.value = bytes(events_as_string, 'utf8')

	def unlock_freezer(self):
		# self.lock_handler.unlock()
		service = self.app.get_services()[0]
		characteristic = service.get_characteristics()[0]
		characteristic.value = bytes('Unlocked', 'utf8')

	def lock_freezer(self):
		# self.lock_handler.lock()
		service = self.app.get_services()[0]
		characteristic = service.get_characteristics()[0]
		characteristic.value = bytes('Locked', 'utf8')

	def test_cryptography(self):
		a_public_key = self.crypt.generate_public_key('public_key.pem')
		an_encrypted_msg = self.crypt.encrypt_message('TEST ENCRYPTED MESSAGE weeeeeeee', a_public_key)
		service = self.app.get_services()[0]
		characteristic = service.get_characteristics()[0]
		characteristic.value = bytes(an_encrypted_msg, 'utf8')


if __name__ == '__main__':
	tropicalia_freezer = TropicaliaFreezer()
	# initialize log with full storage
	tropicalia_freezer.event_logger.add_entry([8, 8, 8, 8], 00)
	storage = tropicalia_freezer.event_logger.get_storage_state()
	storage[3] -= 1
	tropicalia_freezer.event_logger.add_entry(storage, 32)
	storage[1] -= 2
	tropicalia_freezer.event_logger.add_entry(storage, 2)
	storage[0] -= 3
	tropicalia_freezer.event_logger.add_entry(storage, 5)
	try:
		tropicalia_freezer.mainloop.run()
	except KeyboardInterrupt:
		tropicalia_freezer.adv.Release()
