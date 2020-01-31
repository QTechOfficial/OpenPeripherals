import logging

from pydbus import SessionBus
from gi.repository import GLib
from hid import enumerate, Device

from drivers.reddragon import RedDragon
from drivers.fakekeyboard import FakeKeyboard
from interfaces import *

VID = 0x0c45
PID = 0x5004


class KbDaemon:
    DBUS_PATH = '/com/qtech/openperipherals'
    DBUS_SERVICE = 'com.qtech.openperipherals'
    DBUS_INT_LEDS = DBUS_SERVICE + '.Leds'

    def __init__(self):
        # Logging
        self.logger = logging.getLogger('daemon')
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        self.logger.addHandler(sh)

        # DBus
        self.bus = SessionBus()

    def start(self):
        try:
            self.bus.request_name(self.DBUS_SERVICE)
            self.bus.register_object(self.DBUS_PATH, DaemonInterface(), None)
        except RuntimeError:
            self.logger.exception('Failed to connect to DBus')
            exit()

        # List keyboards
        kb_info = self.find_keyboard()
        print(kb_info)

        if kb_info is not None:
            self.logger.info(f'Connecting to keyboard at {kb_info["path"]}')
            rd = RedDragon(Device(path=kb_info['path']))
            self.bus.register_object(self.DBUS_PATH + f'/{kb_info["manufacturer_string"]}', KeyboardInterface(rd), None)
        else:
            self.logger.info(f'Creating fake keyboard')
            fake = FakeKeyboard()
            self.bus.register_object(self.DBUS_PATH + '/fake', KeyboardInterface(fake), None)

        # Start main loop
        GLib.MainLoop().run()

    def find_keyboard(self):
        devices = enumerate(VID, PID)

        for device in devices:
            print(device)
            if device['interface_number'] == 1:
                return device

        return None


if __name__ == '__main__':
    daemon = KbDaemon()
    daemon.start()
