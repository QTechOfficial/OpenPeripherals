import logging

import pydbus
from gi.repository import GLib
from hid import enumerate, Device

from backend.reddragon import RedDragon

VID = 0x0c45
PID = 0x5004

class Keyboard:
    '''
    <node>
        <interface name='com.qtech.openkeyboard.test.properties'>
            <method name='SetBrightness'>
                <arg type='i' name='val' direction='in'/>
                <arg type='s' name='response' direction='out'/>
            </method>
            <method name='SetEffect'>
                <arg type='i' name='val' direction='in'/>
                <arg type='s' name='response' direction='out'/>
            </method>
        </interface>
    </node>
    '''

    def __init__(self, kb):
        self._kb = kb

    def SetBrightness(self, val):
        self._kb.set_brightness(val)
        return 'ok'

    def SetEffect(self, val):
        self._kb.set_effect(val)
        return 'ok'

class KbDaemon:
    def start(self):
        self.logger = logging.getLogger('daemon')
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        self.logger.addHandler(sh)

        # DBUS
        self.bus = pydbus.SessionBus()

        # List keyboards
        kb_path = self.find_keyboard()

        if kb_path is None:
            self.logger.critical('No keyboard found!')
            return
        else:
            self.logger.info(f'Connecting to keyboard at {kb_path}')

        rd = RedDragon(Device(path=kb_path))

        self.bus.publish('com.qtech.openkeyboard.test', Keyboard(rd))

        # Start main loop
        GLib.MainLoop().run()

    def find_keyboard(self):
        devices = enumerate(VID, PID)

        for device in devices:
            print(device)
            if device['interface_number'] == 1:
                return device['path']

        return None


if __name__ == '__main__':
    daemon = KbDaemon()
    daemon.start()
