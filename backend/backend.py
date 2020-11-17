import logging

from dbus import DBus
from gi.repository import GLib
from hid import enumerate, Device

from drivers.reddragon import RedDragon
from drivers.fakekeyboard import FakeKeyboard
from interfaces import *

VID = 0x0c45
PID = 0x5004


class Backend:

    def __init__(self):
        # Logging
        self.logger = logging.getLogger('daemon')
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        self.logger.addHandler(sh)

        # DBus
        self.bus = DBus()

    def start(self):
        # List keyboards
        kb_info = self.find_keyboard()
        print(kb_info)

        if kb_info is not None:
            self.logger.info(f'Connecting to keyboard at {kb_info["path"]}')
            rd = RedDragon(Device(path=kb_info['path']))
            rd.join_bus(kb_info['manufacturer_string'], self.bus)
        else:
            self.logger.info(f'Creating fake keyboard')
            fake = FakeKeyboard()
            rd.join_bus('fake', self.bus)

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
    backend = Backend()
    backend.start()
