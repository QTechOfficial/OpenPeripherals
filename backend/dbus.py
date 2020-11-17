from pydbus import SessionBus

from interfaces import DaemonInterface

class DBus:
    DBUS_PATH = '/com/qtech/openperipherals'
    DBUS_SERVICE = 'com.qtech.openperipherals'

    def __init__(self):
        self.bus = SessionBus()

        try:
            self.bus.request_name(self.DBUS_SERVICE)
            self.bus.register_object(self.DBUS_PATH, DaemonInterface(), None)
        except RuntimeError:
            self.logger.exception('Failed to connect to DBus')
            exit()

    def add_interface(self, path, interface):
        self.bus.register_object(path, interface, None)
