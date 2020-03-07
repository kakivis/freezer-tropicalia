import dbus
import dbus.mainloop.glib
from gi.repository import GObject
from Bluetooth.BluetoothDriver import *

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

	def ReadValue(self, options):
		print('ReadValue: ' + ''.join([str(v) for v in self.value]))
		return self.value

	def WriteValue(self, value, options):
		print('WriteValue: ' + ''.join([str(v) for v in value]))
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


class BleManager:
	def __init__(self):
		dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
		bus = dbus.SystemBus()
		adapter = find_adapter(bus)
		if not adapter:
			print('BLE adapter not found')
			return

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

	def run(self):
		try:
			self.mainloop.run()
		except KeyboardInterrupt:
			self.adv.Release()
