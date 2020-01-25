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


class Commands:
    START_BLOCK = 0x01
    END_BLOCK = 0x02
    SOME_DATA = 0x03
    MORE_DATA = 0x04
    GET_PROPERTY = 0x05
    SET_PROPERTY = 0x06
    READ_HELLA_DATA = 0x07
    WRITE_HELLA_DATA = 0x08
    SMALLER_DATA = 0x09
    DATA_10_BYTES = 0x0A
    GET_KEY_COLORS = 0x10
    SET_KEY_COLORS = 0x11


class Properties:
    EFFECT = 0x00
    BRIGHTNESS = 0x01
    SPEED = 0x02
    DIRECTION = 0x03
    RAINBOW = 0x04
    EFFECT_COLOR = 0x05
    SOME_COLOR = 0x09


class RedDragon:
    def __init__(self, hid):
        self._hid = hid

    def write_packet(self, cmd, size=1, offset=0, *data):
        cksum = cmd

        for dat in data:
            cksum += dat

        # Packet structure: [Header(4), Checksum, Padding?, Command, Size, OffsetL, OffsetH, Padding(0), ...]
        self._hid.write(bytes([4, cksum & 0xFF, 0, cmd, size, offset & 0x00FF, offset >> 8 & 0x00FF, 0] + list(data)))
        resp = self._hid.read(128, 10)
        # Hidapi seems to be bad at freeing things or something because a bunch of garbage gets tacked on to the
        # end of the responses. I just cut out the parts that are valid based on the size argument.
        resp_len = resp[4]
        return tuple(resp[8:8+resp_len])

    def set_property(self, prop_id, *values):
        self.write_packet(Commands.START_BLOCK)
        self.write_packet(Commands.SET_PROPERTY, len(values), prop_id, *values)
        self.write_packet(Commands.END_BLOCK)

    def get_property(self, prop_id, size=1):
        self.write_packet(Commands.START_BLOCK)
        resp = self.write_packet(Commands.GET_PROPERTY, size, prop_id)
        self.write_packet(Commands.END_BLOCK)
        return resp

    def set_effect(self, effect):
        # TODO: Check argument
        self.set_property(Properties.EFFECT, effect)

    def get_effect(self):
        return self.get_property(Properties.EFFECT)[0]

    def set_brightness(self, brightness):
        # TODO: Check argument
        self.set_property(Properties.BRIGHTNESS, brightness)

    def get_brightness(self):
        return self.get_property(Properties.BRIGHTNESS)[0]

    def set_speed(self, speed):
        # TODO: Check argument
        self.set_property(Properties.SPEED, speed)

    def get_speed(self):
        return self.get_property(Properties.SPEED)[0]

    def set_direction(self, direction):
        # TODO: Check argument
        self.set_property(Properties.DIRECTION, direction)

    def get_direction(self):
        return self.get_property(Properties.DIRECTION)[0] == 1

    def set_rainbow(self, rainbow):
        # TODO: Check argument
        self.set_property(Properties.RAINBOW, rainbow)

    def get_rainbow(self):
        return self.get_property(Properties.RAINBOW)[0] == 1

    def set_effect_color(self, color):
        # TODO: Check argument
        self.set_property(Properties.EFFECT_COLOR, *color)

    def get_effect_color(self):
        return self.get_property(Properties.EFFECT_COLOR, 3)

    def set_color_data(self, offset, data):
        # TODO: Check argument
        self.write_packet(Commands.SET_KEY_COLORS, len(data), offset, *data)

    def get_color_data(self, size=0x36, offset=0x00):
        # TODO: Check argument
        resp = self.write_packet(Commands.GET_KEY_COLORS, size, offset)
        return resp

    def set_key_color(self, key_id, color):
        # TODO: TEMP
        magic_dict = {}
        self.set_color_data(magic_dict[key_id], color)

    def get_key_color(self, key_id):
        # TODO: TEMP
        magic_dict = {}
        return self.get_color_data(3, magic_dict[key_id])


    # TODO: Find out what this actually does
    def set_some_color(self, r, g, b):
        # TODO: Check to see if the 3 is important, if not, switch to set_property
        self.set_property(Properties.SOME_COLOR, r, g, b)

    def get_some_color(self):
        return self.get_property(Properties.SOME_COLOR, 3)

    def set_all_colors(self, color):
        # TODO: Implement
        pass

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

        self.write_packet(Commands.START_BLOCK)
        colors_raw = self.get_color_data(0x36, 0x00)
        colors_raw += self.get_color_data(0x36, 0x36)
        colors_raw += self.get_color_data(0x36, 0x6C)
        colors_raw += self.get_color_data(0x36, 0xA2)
        colors_raw += self.get_color_data(0x36, 0xD8)
        colors_raw += self.get_color_data(0x36, 0x10E)
        colors_raw += self.get_color_data(0x36, 0x144)
        self.write_packet(Commands.END_BLOCK)
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

        # TODO: If only there was some kind of testing framework I could use instead of this shit... Hmmm
        print('Effects')
        for i in range(15):
            rd.set_effect(i)
            print(i, rd.get_effect() == i)
            time.sleep(0.1)

        print('Brightness')
        for i in range(6):
            rd.set_brightness(i)
            print(i, rd.get_brightness() == i)
            time.sleep(0.1)

        print('Speed')
        for i in range(6):
            rd.set_speed(i)
            print(i, rd.get_speed() == i)
            time.sleep(0.1)

        print('Direction')
        rd.set_direction(True)
        time.sleep(0.1)
        print(rd.get_direction() == True)
        rd.set_direction(False)
        time.sleep(0.1)
        print(rd.get_direction() == False)

        print('Rainbow')
        rd.set_rainbow(True)
        time.sleep(0.1)
        print(rd.get_rainbow() == True)
        rd.set_rainbow(False)
        time.sleep(0.1)
        print(rd.get_rainbow() == False)

        print('Effect Color')
        rd.set_effect_color(255, 0, 0)
        time.sleep(0.1)
        print(rd.get_effect_color() == (255, 0, 0))
        rd.set_effect_color(0, 255, 0)
        time.sleep(0.1)
        print(rd.get_effect_color() == (0, 255, 0))
        rd.set_effect_color(0, 0, 255)
        time.sleep(0.1)
        print(rd.get_effect_color() == (0, 0, 255))

        print('Color Data')
        rd.set_effect(0x14)
        rd.set_color_data(0, [255, 0, 0, 0, 255, 0, 0, 0, 255])
        print(rd.get_color_data(9, 0) == (255, 0, 0, 0, 255, 0, 0, 0, 255))

        print('Some Color')
        rd.set_some_color(255, 0, 0)
        print(rd.get_some_color() == (255, 0, 0))
