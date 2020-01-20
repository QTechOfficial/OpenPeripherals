from pprint import pprint as pp
from random import randint
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
        self._hid.read(256, 10)
        self._hid.write(bytes([4, 2, 0, 2]))  # End block
        self._hid.read(256, 10)

    def set_effect(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 0, 0, 0, val]))

    def set_brightness(self, val):
        # TODO: Check argument
        self.write_packet(6, bytes([1, 1, 0, 0, val]))

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

    def set_some_color(self, r, g, b):
        self.write_packet(6, bytes([3, 9, 0, 0, r, g, b]))


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
