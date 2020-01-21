import logging

from pydbus import SessionBus
from gi.repository import GLib
from hid import enumerate, Device

from backend.reddragon import RedDragon

VID = 0x0c45
PID = 0x5004

# TODO: Why do I need this?
class DaemonInterface:
    '''
    <node>
        <interface name='com.qtech.openkeyboard'>
        </interface>
    </node>
    '''

class KeyboardInterface:
    '''
    <node>
        <interface name='com.qtech.openkeyboard.Leds'>
            <method name='SetBrightness'>
                <arg type='i' name='brightness' direction='in' />
            </method>
            <method name='SetEffect'>
                <arg type='i' name='effect' direction='in' />
            </method>
            <method name='SetEffectColor'>
                <arg type='i' name='r' direction='in' />
                <arg type='i' name='g' direction='in' />
                <arg type='i' name='b' direction='in' />
            </method>
            <method name='SetKeyColor'>
                <arg type='i' name='idx' direction='in' />
                <arg type='i' name='r' direction='in' />
                <arg type='i' name='g' direction='in' />
                <arg type='i' name='b' direction='in' />
            </method>
        </interface>
    </node>
    '''

    def __init__(self, kb):
        self._kb = kb

    def SetBrightness(self, brightness):
        self._kb.set_brightness(brightness)

    def SetEffect(self, effect):
        self._kb.set_effect(effect)

    def SetEffectColor(self, r, g, b):
        self._kb.set_effect_color(r, g, b)

    def SetKeyColor(self, idx, r, g, b):
        self._kb.set_color_data(idx * 3, bytes([r, g, b]))

class KbDaemon:
    def __init__(self):
        self.logger = logging.getLogger('daemon')
        self.logger.setLevel(logging.DEBUG)

        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)

        self.logger.addHandler(sh)

    def start(self):
        # DBUS
        self.bus = SessionBus()
        try:
            self.bus.request_name('com.qtech.openkeyboard')
            self.bus.register_object('/com/qtech/openkeyboard', DaemonInterface(), None)
        except RuntimeError:
            self.logger.exception('Failed to connect to DBus')
            exit()

        # List keyboards
        kb_info = self.find_keyboard()
        print(kb_info)

        if kb_info is None:
            self.logger.critical('No keyboard found!')
            exit()
        else:
            self.logger.info(f'Connecting to keyboard at {kb_info["path"]}')

        rd = RedDragon(Device(path=kb_info['path']))
        self.bus.register_object(f'/com/qtech/openkeyboard/{kb_info["manufacturer_string"]}', KeyboardInterface(rd), None)

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
