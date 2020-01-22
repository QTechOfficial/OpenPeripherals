class FakeKeyboard:
    def __init__(self):
        self._brightness = 0
        self._effect = 0
        self._speed = 0
        self._direction = False
        self._rainbow = False
        self._effect_color = (0, 0, 0)

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

    def set_effect_color(self, r, g, b):
        # TODO: Check argument
        self._effect_color = (r, g, b)

    def get_effect_color(self):
        return self._effect_color

    def set_color_data(self, offset, data):
        # TODO: Check argument
        pass

    def get_all_colors(self):
        # TODO: Impliment
        pass
