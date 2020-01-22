from pprint import pprint as pp
from random import randint
from struct import unpack_from
import hid
import time
import colorsys

packet = [
    '04 01 00 01',
    '04 11 01 06 03 09 00 00 0000ff0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    '04 37 10 11 36 00 00 00 0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000000000ff0000ff0000ff0000000000',
    '04 6e 0f 11 36 36 00 00 0000000000000000000000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff00ffff0000ff0000',
    '04 a1 12 11 36 6c 00 00 0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ffff00ff0000ff0000',
    '04 d7 12 11 36 a2 00 00 0000ff00ffff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff0000ff00ffff0000ff0000',
    '04 13 0d 11 36 d8 00 00 0000ff0000ff0000ff0000000000ff0000000000000000000000ff0000ff0000ff0000000000ff0000000000ff0000ffff00ff0000ff0000',
    '04 47 0f 11 36 0e 01 00 0000ff0000ff0000ff0000ff0000ff0000ff0000000000ff0000000000ff0000000000ff0000ff0000ff0000ff0000ff0000ff0000ff0000',
    '04 81 0b 11 36 44 01 00 0000ff0000ff0000ff0000ff0000ff0000ff0000000000000000000000000000000000ff0000ff0000ff0000000000ff00ffff0000000000',
    '04 c2 00 11 36 7a 01 00 0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    '04 02 00 02',
]


def phex(data):
    print(' '.join([hex(d) for d in data]))


class RedDragon:
    def __init__(self, hid):
        self._hid = hid
        self._brightness = 0
        self._effect = 0

    def write_packet(self, cmd, data=bytes()):
        cksum = cmd

        for dat in data:
            cksum += dat

        self._hid.write(bytes([4, 1, 0, 1]))  # Start block
        self._hid.read(256, 10)
        ledata = bytes([4, cksum & 0xFF, 0, cmd]) + data
        #print(len(ledata))
        #phex(ledata)
        self._hid.write(ledata)
        resp = self._hid.read(256, 10)
        self._hid.write(bytes([4, 2, 0, 2]))  # End block
        self._hid.read(256, 10)

        return resp

    def set_effect(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 0, 0, 0, val]))
        self._effect = val

    def get_effect(self):
        # TODO: Actually get from keyboard
        return self._effect

    def set_brightness(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 1, 0, 0, val]))
        self._brightness = val

    def get_brightness(self):
        # TODO: Actually get from keyboard
        return self._brightness

    def set_speed(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 2, 0, 0, val]))

    def set_direction(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 3, 0, 0, val]))

    def set_rainbow_puke(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 4, 0, 0, val]))

    def set_effect_color(self, r, g, b):
        # TODO: Check argument
        self.write_packet(6, bytes([3, 5, 0, 0, r, g, b]))

    def set_color_data(self, offset, data):
        # TODO: Check argument
        self.write_packet(0x11, bytes([len(data), offset & 0x00FF, offset >> 8 & 0x00FF, 0]) + data)

    def get_color_data(self, size=0x36, offset=0x00):
        # TODO: Check argument
        resp = self.write_packet(0x10, bytes([size, offset & 0x00FF, offset >> 8 & 0x00FF, 0]))
        # Hidapi seems to be bad at freeing things or something because a bunch of garbage gets tacked on to the
        # end of the responses. I just cut out the parts that are valid based on the size argument.
        colors_raw = resp[8:8+size]
        return colors_raw

    def set_some_color(self, r, g, b):
        self.write_packet(6, bytes([3, 9, 0, 0, r, g, b]))

    def get_all_colors(self):
        colors = {}

        # Temporary - Horrible garbage for testing
        keys = ['ESC', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '<BLANK>', 'PRTSC', 'SCLK', 'PAUSE', '<BLANK>', '<BLANK>', '<BLANK>', '<BLANK>']
        keys += ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'BACKSP', 'INS', 'HOME', 'PGUP', '<BLANK>', '<BLANK>', '<BLANK>', '<BLANK>']
        keys += ['TAB', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\', 'DEL', 'END', 'PGDN', '<BLANK>', '<BLANK>', '<BLANK>', '<BLANK>']
        keys += ['CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'RETURN']
        keys += ['SHIFT', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'RSHIFT', '<BLANK>', '<BLANK>', '<BLANK>', '<BLANK>']
        # keys += ['ESC', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', '<BLANK>', 'PRTSC', 'SCLK', 'PAUSE']
        colors = []

        colors_raw = self.get_color_data(0x36, 0x00)
        colors_raw += self.get_color_data(0x36, 0x36)
        colors_raw += self.get_color_data(0x36, 0x6C)
        colors_raw += self.get_color_data(0x36, 0xA2)
        colors_raw += self.get_color_data(0x36, 0xD8)
        colors_raw += self.get_color_data(0x36, 0x10E)
        colors_raw += self.get_color_data(0x36, 0x144)
        phex(colors_raw)

        for i in range(0, len(colors_raw), 3):
            colors.append(colors_raw[i:i+3])

        return dict(zip(keys, colors[:len(keys)]))


if __name__ == '__main__':
    with hid.Device(path=b'/dev/hidraw6') as h:
        print(f'Manufac: {h.manufacturer}')
        print(f'Prod: {h.product}')
        print(f'Ser: {h.serial}')

        rd = RedDragon(h)

        rd.set_effect(0x14)

        #rd.set_some_color(255, 0, 0)

        for i in range(0x7D):
            rd.set_color_data(i * 3, bytes([255, 0, 0]))

        time.sleep(2)

        #for i in range(0x7D):
        #    rd.set_color_data(0x36*2, bytes([255 - int(i/0x7D*0xFF), 0, int(i/0x7D*0xFF)]*(i+1)))
            #time.sleep(0.1)

        #rd.set_some_color(255, 0, 0)
