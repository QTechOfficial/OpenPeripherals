from led import Led
from utils import set_button_color

class Key(Led):
    def __init__(self, name, button, led_offset):
        Led.__init__(self)
        self.name = name
        self.button = button
        self.led_offset = led_offset

    def set_color(self, color):
        self.color = color
        set_button_color(self.button, color)
