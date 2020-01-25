from backend.drivers.fakekeyboard import FakeKeyboard

class TestClass:
    def setup(self):
        self.kb = FakeKeyboard()
        
    # It's gamer time
    def effects(self):
        for i in range(15):
            self.kb.set_effect(i)
            assert self.kb.get_effect() == i,"Failed to get effect {i}"

    def brightness(self):
        for i in range(6):
            self.kb.set_brightness(i)
            assert self.kb.get_brightness() == i,"Failed to get brightness ${i}"

    def speed(self):
        for i in range(6):
            self.kb.set_speed(i)
            assert self.kb.get_speed() == i,"Failed to get speed ${i}"

    def direction(self):
        self.kb.set_direction(True)
        assert self.kb.get_direction() == True,"Failed to set direction to True"
        
        self.kb.set_direction(False)
        assert self.kb.get_direction() == False,"Failed to set direction to False"

    def rainbow(self):
        self.kb.set_rainbow(True)
        assert self.kb.get_rainbow() == True,"Failed to set rainbow to True"
        
        self.kb.set_rainbow(False)
        assert self.kb.get_rainbow() == False,"Failed to set rainbow to False"

    def colors(self):
        self.kb.set_effect_color(255, 0, 0)
        assert self.kb.get_effect_color() == (255, 0, 0),"Failed to set color to 255,0,0"
        
        self.kb.set_effect_color(0, 255, 0)
        assert self.kb.get_effect_color() == (0, 255, 0),"Failed to set color to 0,255,0"

        self.kb.set_effect_color(0, 0, 255) 
        assert self.kb.get_effect_color() == (0, 0, 255),"Failed to set color to 0,0,255"
    
    def key_color(self):
        self.kb.set_key_color('A', (255, 0, 0))
        assert self.kb.get_key_color('A') == (255, 0, 0),"Failed to set key color to 255,0,0"

        self.kb.set_key_color('A', (0, 255, 0))
        assert self.kb.get_key_color('A') == (0, 255, 0),"Failed to set key color to 0,255,0"

        self.kb.set_key_color('A', (0, 0, 255))
        assert self.kb.get_key_color('A') == (0, 0, 255),"Failed to set key color to 0,0,255"

    def key_color_all(self):
        self.kb.set_all_colors({'A': (255, 0, 0), 'B': (0, 255, 0), 'C': (0, 0, 255)})
        lotsofcolors = self.kb.get_all_colors()

        assert lotsofcolor['A'] == (255, 0, 0),"Failed to set all colors on key A to 255,0,0"
        assert lotsofcolor['B'] == (0, 255, 0),"Failed to set all colors on key B to 0,255,0"
        assert lotsofcolor['C'] == (0, 0, 255),"Failed to set all colors on key C to 0,0,255"
