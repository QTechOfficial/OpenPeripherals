from backend.daemon import KbDaemon

class TestClass:
    def test(self):
        kb = KbDaemon()
        assert kb.logger
