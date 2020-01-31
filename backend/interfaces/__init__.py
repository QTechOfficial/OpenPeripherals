class DaemonInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals'>
        </interface>
    </node>
    '''

class KeyboardInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals.Leds'>
            <method name='SetEffect'>
                <arg type='i' name='effect' direction='in' />
            </method>
            <method name='GetEffect'>
                <arg type='i' name='effect' direction='out' />
            </method>
            <method name='SetBrightness'>
                <arg type='i' name='brightness' direction='in' />
            </method>
            <method name='GetBrightness'>
                <arg type='i' name='brightness' direction='out' />
            </method>
            <method name='SetSpeed'>
                <arg type='i' name='speed' direction='in' />
            </method>
            <method name='GetSpeed'>
                <arg type='i' name='speed' direction='out' />
            </method>
            <method name='SetDirection'>
                <arg type='b' name='direction' direction='in' />
            </method>
            <method name='GetDirection'>
                <arg type='b' name='direction' direction='out' />
            </method>
            <method name='SetRainbow'>
                <arg type='b' name='rainbow' direction='in' />
            </method>
            <method name='GetRainbow'>
                <arg type='b' name='rainbow' direction='out' />
            </method>
            <method name='SetEffectColor'>
                <arg type='i' name='r' direction='in' />
                <arg type='i' name='g' direction='in' />
                <arg type='i' name='b' direction='in' />
            </method>
            <method name='GetEffectColor'>
                <arg type='i' name='r' direction='out' />
                <arg type='i' name='g' direction='out' />
                <arg type='i' name='b' direction='out' />
            </method>
            <method name='SetKeyColor'>
                <arg type='s' name='idx' direction='in' />
                <arg type='i' name='r' direction='in' />
                <arg type='i' name='g' direction='in' />
                <arg type='i' name='b' direction='in' />
            </method>
            <method name='GetKeyColor'>
                <arg type='s' name='idx' direction='in' />
                <arg type='i' name='r' direction='out' />
                <arg type='i' name='g' direction='out' />
                <arg type='i' name='b' direction='out' />
            </method>
            <method name='SetAllColors'>
                <arg type='a{s(iii)}' name='colors' direction='in' />
            </method>
            <method name='GetAllColors'>
                <arg type='a{s(iii)}' name='colors' direction='out' />
            </method>
        </interface>
    </node>
    '''

    def __init__(self, kb):
        self._kb = kb

    def SetEffect(self, effect):
        self._kb.set_effect(effect)

    def GetEffect(self):
        return self._kb.get_effect()

    def SetBrightness(self, brightness):
        self._kb.set_brightness(brightness)

    def GetBrightness(self):
        return self._kb.get_brightness()

    def SetSpeed(self, speed):
        self._kb.set_speed(speed)

    def GetSpeed(self):
        return self._kb.get_speed()

    def SetDirection(self, direction):
        self._kb.set_direction(direction)

    def GetDirection(self):
        return self._kb.get_direction()

    def SetRainbow(self, rainbow):
        self._kb.set_rainbow(rainbow)

    def GetRainbow(self):
        return self._kb.get_rainbow()

    def SetEffectColor(self, r, g, b):
        self._kb.set_effect_color(r, g, b)

    def GetEffectColor(self):
        return self._kb.get_effect_color()

    def SetKeyColor(self, idx, r, g, b):
        self._kb.set_key_color(idx, r, g, b)

    def GetKeyColor(self, idx):
        return self._kb.get_key_color(idx)

    def SetAllColors(self, colors):
        self._kb.set_all_colors(colors)

    def GetAllColors(self):
        return self._kb.get_all_colors()
