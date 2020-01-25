from backend.drivers.fakekeyboard import FakeKeyboard

class TestClass:
    def setup(self):
        self.kb = FakeKeyboard()
    
    def test_brightness(self):
        self.kb.set_brightness(5)
        assert self.kb.get_brightness() == 5
