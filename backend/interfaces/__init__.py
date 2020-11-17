class DaemonInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals'>
        </interface>
    </node>
    '''


class EffectInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals.Effect'>
            <method name='SetEffect'>
                <arg type='i' name='effect' direction='in' />
            </method>
            <method name='GetEffect'>
                <arg type='i' name='effect' direction='out' />
            </method>
            <method name='SetEffectColor'>
                <arg type='(iii)' name='color' direction='in' />
            </method>
            <method name='GetEffectColor'>
                <arg type='(iii)' name='color' direction='out' />
            </method>
            <method name='SetRainbow'>
                <arg type='b' name='rainbow' direction='in' />
            </method>
            <method name='GetRainbow'>
                <arg type='b' name='rainbow' direction='out' />
            </method>
        </interface>
    </node>
    '''

    def __init__(self, peripheral):
        self._peripheral = peripheral

    def SetEffect(self, effect):
        self._peripheral.set_effect(effect)

    def GetEffect(self):
        return self._peripheral.get_effect()

    def SetEffectColor(self, color):
        self._peripheral.set_effect_color(color)

    def GetEffectColor(self):
        return self._peripheral.get_effect_color()

    def SetRainbow(self, rainbow):
        self._peripheral.set_rainbow(rainbow)

    def GetRainbow(self):
        return self._peripheral.get_rainbow()


class DimmableInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals.Dimmable'>
            <method name='SetBrightness'>
                <arg type='i' name='brightness' direction='in' />
            </method>
            <method name='GetBrightness'>
                <arg type='i' name='brightness' direction='out' />
            </method>
        </interface>
    </node>
    '''

    def __init__(self, peripheral):
        self._peripheral = peripheral

    def SetBrightness(self, brightness):
        self._peripheral.set_brightness(brightness)

    def GetBrightness(self):
        return self._peripheral.get_brightness()


class AnimationInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals.Animation'>
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
        </interface>
    </node>
    '''

    def __init__(self, peripheral):
        self._peripheral = peripheral

    def SetSpeed(self, speed):
        self._peripheral.set_speed(speed)

    def GetSpeed(self):
        return self._peripheral.get_speed()

    def SetDirection(self, direction):
        self._peripheral.set_direction(direction)

    def GetDirection(self):
        return self._peripheral.get_direction()


class KeyboardInterface:
    '''
    <node>
        <interface name='com.qtech.openperipherals.Keyboard'>
            <method name='SetKeyColor'>
                <arg type='s' name='idx' direction='in' />
                <arg type='(iii)' name='color' direction='in' />
            </method>
            <method name='GetKeyColor'>
                <arg type='s' name='idx' direction='in' />
                <arg type='(iii)' name='color' direction='out' />
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

    def __init__(self, peripheral):
        self._peripheral = peripheral

    def SetKeyColor(self, idx, color):
        self._peripheral.set_key_color(idx, color)

    def GetKeyColor(self, idx):
        return self._peripheral.get_key_color(idx)

    def SetAllColors(self, colors):
        self._peripheral.set_all_colors(colors)

    def GetAllColors(self):
        return self._peripheral.get_all_colors()

