from objects.color import Color
from utils import set_button_color

class Key:
    def __init__(self, name, button, led_offset):
        self.name = name
        self.button = button
        self.led_offset = led_offset
        self.color = Color(255, 255, 255)

    def set_color(self, color):
        self.color = color
        set_button_color(self.button, color)
