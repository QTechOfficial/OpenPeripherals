from abc import ABC

class Keyboard(ABC):
    def join_bus(self, bus):
        pass

    def set_effect(self, val):
        pass

    def get_effect(self):
        pass

    def set_brightness(self, val):
        pass

    def get_brightness(self):
        pass

    def set_speed(self, val):
        pass

    def get_speed(self):
        pass

    def set_direction(self, val):
        pass

    def get_direction(self):
        pass

    def set_rainbow(self, val):
        pass

    def get_rainbow(self):
        pass

    def set_effect_color(self, color):
        pass

    def get_effect_color(self):
        pass

    def set_key_color(self, key_id, color):
        pass

    def get_key_color(self, key_id):
        pass

    def set_all_colors(self, colors):
        pass

    def get_all_colors(self):
        pass
