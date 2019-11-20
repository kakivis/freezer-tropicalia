import sys
import dbus, dbus.mainloop.glib
from gi.repository import GObject
from BluetoothDriver import *

GATT_CHRC_IFACE = 'org.bluez.GattCharacteristic1'
TROPICALIA_SERVICE_UUID = '12345678-1234-5678-1234-56789abcdef0'
TEST_CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef1'
TEST_ENCRYPT_CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef2'
TEST_SECURE_CHARACTERISTIC_UUID = '12345678-1234-5678-1234-56789abcdef3'
LOCAL_NAME = 'TropilaciaFreezer'
mainloop = None


class TestCharacteristic(Characteristic):
	def __init__(self, bus, index, service):
		Characteristic.__init__(
			self, bus, index,
			TEST_CHARACTERISTIC_UUID,
			['read', 'write', 'writable-auxiliaries'],
			service)
		self.value = []

	def ReadValue(self, options):
		print('TestCharacteristic Read: ' + repr(self.value))
		return self.value

	def WriteValue(self, value, options):
		print('TestCharacteristic Write: ' + repr(value))
		self.value = value


class TestEncryptCharacteristic(Characteristic):
	def __init__(self, bus, index, service):
		Characteristic.__init__(
			self, bus, index,
			TEST_ENCRYPT_CHARACTERISTIC_UUID,
			['encrypt-read', 'encrypt-write'],
			service)
		self.value = []

	def ReadValue(self, options):
		print('TestEncryptCharacteristic Read: ' + repr(self.value))
		return self.value

	def WriteValue(self, value, options):
		print('TestEncryptCharacteristic Write: ' + repr(value))
		self.value = value


class TestSecureCharacteristic(Characteristic):
	def __init__(self, bus, index, service):
		Characteristic.__init__(
			self, bus, index,
			TEST_SECURE_CHARACTERISTIC_UUID,
			['secure-read', 'secure-write'],
			service)
		self.value = []

	def ReadValue(self, options):
		print('TestSecureCharacteristic Read: ' + repr(self.value))
		return self.value

	def WriteValue(self, value, options):
		print('TestSecureCharacteristic Write: ' + repr(value))
		self.value = value


class TropicaliaService(Service):
	def __init__(self, bus, index):
		Service.__init__(self, bus, index, TROPICALIA_SERVICE_UUID, True)
		self.add_characteristic(TestCharacteristic(bus, 0, self))
		self.add_characteristic(TestEncryptCharacteristic(bus, 1, self))
		self.add_characteristic(TestSecureCharacteristic(bus, 2, self))


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


def main():
	global mainloop
	dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()
	adapter = find_adapter(bus)
	if not adapter:
		print('BLE adapter not found')
		return

	service_manager = dbus.Interface(
		bus.get_object(BLUEZ_SERVICE_NAME, adapter),
		GATT_MANAGER_IFACE)
	ad_manager = dbus.Interface(
		bus.get_object(BLUEZ_SERVICE_NAME, adapter),
		LE_ADVERTISING_MANAGER_IFACE)

	app = TropicaliaApplication(bus)
	adv = TropicaliaAdvertisement(bus, 0)

	mainloop = GObject.MainLoop()

	service_manager.RegisterApplication(app.get_path(), {},
		reply_handler=register_app_cb,
		error_handler=register_app_error_cb)
	ad_manager.RegisterAdvertisement(adv.get_path(), {},
		reply_handler=register_ad_cb,
		error_handler=register_ad_error_cb)
	try:
		mainloop.run()
	except KeyboardInterrupt:
		adv.Release()


if __name__ == '__main__':
	main()
