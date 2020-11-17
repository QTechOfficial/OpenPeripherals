from .keyboard import Keyboard

class FakeKeyboard(Keyboard):
    def __init__(self):
        self._brightness = 0
        self._effect = 0
        self._speed = 0
        self._direction = False
        self._rainbow = False
        self._effect_color = (0, 0, 0)
        self._colors = {}

    def join_bus(self, name, bus):
        bus.add_interface(f'{bus.DBUS_PATH}/{name}/effect', EffectInterface(self))
        bus.add_interface(f'{bus.DBUS_PATH}/{name}/dimmable', DimmableInterface(self))
        bus.add_interface(f'{bus.DBUS_PATH}/{name}/animation', AnimationInterface(self))
        bus.add_interface(f'{bus.DBUS_PATH}/{name}/keyboard', KeyboardInterface(self))

    def set_effect(self, val):
        # TODO: Check argument
        self._effect = val

    def get_effect(self):
        # TODO: Actually get from keyboard
        return self._effect

    def set_brightness(self, val):
        # TODO: Check argument
        self._brightness = val

    def get_brightness(self):
        # TODO: Actually get from keyboard
        return self._brightness

    def set_speed(self, val):
        # TODO: Check argument
        self._speed = val

    def get_speed(self):
        return self._speed

    def set_direction(self, val):
        # TODO: Check argument
        self._direction = val

    def get_direction(self):
        return self._direction

    def set_rainbow(self, val):
        # TODO: Check argument
        self._rainbow = val

    def get_rainbow(self):
        return self._rainbow

    def set_effect_color(self, color):
        # TODO: Check argument
        self._effect_color = color

    def get_effect_color(self):
        return self._effect_color

    def set_key_color(self, key_id, color):
        # TODO: Check argument
        self._colors[key_id] = color

    def get_key_color(self, key_id):
        return self._colors[key_id]

    def set_all_colors(self, colors):
        self._colors = colors

    def get_all_colors(self):
        return self._colors
