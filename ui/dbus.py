from pydbus import SessionBus
from xml.etree import ElementTree


class DBus:
    DBUS_PATH = '/com/qtech/openperipherals'
    DBUS_SERVICE = 'com.qtech.openperipherals'

    def __init__(self):
        self.bus = SessionBus()

    def get_interface(self, device, interface):
        return self.bus.get(self.DBUS_SERVICE, f'{self.DBUS_PATH}/{device}/{interface}')

    def get_devices(self):
        devices = []

        service = self.bus.get(self.DBUS_SERVICE)
        xml_str = service.Introspect()
        for child in ElementTree.fromstring(xml_str):
            if child.tag == 'node':
                devices.append(child.attrib['name'])

        return devices
