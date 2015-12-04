import platform
import sys
import unittest


from fetchdata.output import fetchdataStream


class TestWindows(unittest.TestCase):


    def setUp(self):
        if platform.system() != 'Windows':
            self.skipTest('This test is for windows-specific behavior.')


    def test_colorOutput(self):
        """
        Color output functions on windows
        """
        import colorama
        gs = fetchdataStream(sys.stdout, override_appveyor=True)
        self.assertTrue(issubclass(type(gs.stream),
                        colorama.ansitowin32.StreamWrapper))

