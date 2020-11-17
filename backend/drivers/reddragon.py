from .keyboard import Keyboard

def phex(data):
    print(' '.join([hex(d) for d in data]))


class Commands:
    START_BLOCK = 0x01
    END_BLOCK = 0x02
    SOME_DATA = 0x03    # Seems related to lights off 0x2C bytes of data
    MORE_DATA = 0x04    # Seems related to lights on
    GET_PROPERTY = 0x05
    SET_PROPERTY = 0x06
    READ_HELLA_DATA = 0x07
    WRITE_HELLA_DATA = 0x08
    SMALLER_DATA = 0x09
    DATA_10_BYTES = 0x0A
    POSSIBLY_LAYOUT = 0x0F
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


class RedDragon(Keyboard):
    def __init__(self, hid):
        self._hid = hid
        self.magic_dict = {'ESCAPE': 0, 'F1': 3, 'F2': 6, 'F3': 9, 'F4': 12, 'F5': 15, 'F6': 18, 'F7': 21, 'F8': 24, 'F9': 27, 'F10': 30, 'F11': 33, 'F12': 36, 'PRTSC': 42, 'SCLK': 45, 'PAUSE': 48, 'GRAVE': 63, '1': 66, '2': 69, '3': 72, '4': 75, '5': 78, '6': 81, '7': 84, '8': 87, '9': 90, '0': 93, 'MINUS': 96, 'EQUALS': 99, 'BACK': 102, 'INSERT': 105, 'HOME': 108, 'PGUP': 111, 'TAB': 126, 'Q': 129, 'W': 132, 'E': 135, 'R': 138, 'T': 141, 'Y': 144, 'U': 147, 'I': 150, 'O': 153, 'P': 156, 'LBRACKET': 159, 'RBRACKET': 162, 'RETURN': 228, 'DEL': 168, 'END': 171, 'PGDN': 174, 'CAPSLK': 189, 'A': 192, 'S': 195, 'D': 198, 'F': 201, 'G': 204, 'H': 207, 'J': 210, 'K': 213, 'L': 216, 'SEMICOLON': 219, 'APOSTROPHE': 222, 'BACKSLASH': 165, 'SHIFT': 252, 'Z': 258, 'X': 261, 'C': 264, 'V': 267, 'B': 270, 'N': 273, 'M': 276, 'COMMA': 279, 'PERIOD': 282, 'SLASH': 285, 'RSHIFT': 291, 'CONTROL': 315, 'META': 318, 'ALT': 321, 'SPACE': 324, 'RALT': 327, 'FN': 330, 'APP': 333, 'RCONTROL': 339, 'NUMLOCK': 114, 'NUMSLASH': 117, 'NUMSTAR': 120, 'NUMMINUS': 123, 'NUM7': 177, 'NUM8': 180, 'NUM9': 183, 'NUM4': 240, 'NUM5': 243, 'NUM6': 246, 'NUMPLUS': 186, 'NUM1': 303, 'NUM2': 306, 'NUM3': 309, 'NUM0': 369, 'NUMPERIOD': 372, 'NUMENTER': 312, 'UP': 297, 'LEFT': 357, 'DOWN': 360, 'RIGHT': 363}

    def write_packet(self, cmd, size=1, offset=0, *data):
        cksum = cmd

        for dat in data:
            cksum += dat

        # Packet structure: [Header(4), Checksum, Padding?, Command, Size, OffsetL, OffsetH, Padding(0), ...]
        self._hid.write(bytes([4, cksum & 0xFF, 0, cmd, size, offset & 0x00FF, offset >> 8 & 0x00FF, 0] + list(data)))
        resp = self._hid.read(128, 100)
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
        # What the RedDragon called speed is actually delay between frames, so flip the range from 0-5 to 5-0
        self.set_property(Properties.SPEED, 5 - speed)

    def get_speed(self):
        # What the RedDragon called speed is actually delay between frames, so flip the range from 0-5 to 5-0
        return 5 - self.get_property(Properties.SPEED)[0]

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
        self.set_color_data(self.magic_dict[key_id], color)

    def get_key_color(self, key_id):
        return self.get_color_data(3, self.magic_dict[key_id])

    # TODO: Find out what this actually does
    def set_some_color(self, color):
        self.set_property(Properties.SOME_COLOR, color)

    def get_some_color(self):
        return self.get_property(Properties.SOME_COLOR, 3)

    def set_all_colors(self, colors):
        color_data = [0] * 0x17A  # Fill the entire region with zeros
        for key_id, color in colors.items():
            key_offset = self.magic_dict[key_id]
            color_data[key_offset:key_offset+3] = color

        # Break the color data into chunks of length 0x36
        chunks = []
        for i in range(0, len(color_data), 0x36):
            chunks.append(color_data[i:i + 0x36])

        # Send each chunk to the keyboard
        self.write_packet(Commands.START_BLOCK)
        for i, chunk in enumerate(chunks):
            chunk_len = len(chunk)
            self.set_color_data(i * chunk_len, chunk)
        self.write_packet(Commands.END_BLOCK)

    def get_all_colors(self):
        colors = {}

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

        for key_id, offset in self.magic_dict.items():
            colors[key_id] = tuple(colors_raw[offset:offset+3])

        return colors
