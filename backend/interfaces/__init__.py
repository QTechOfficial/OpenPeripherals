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
            <method name='GetAll'>
                <arg type='a{s(iii)}' name='colors' direction='out' />
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

    def GetAll(self):
        return self._kb.get_all_colors()
