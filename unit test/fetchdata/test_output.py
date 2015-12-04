from __future__ import unicode_literals
import sys
import unittest

try:
    from io import StringIO
except:
    from StringIO import StringIO

from fetchdata.output import Colors, fetchdataStream, debug
import fetchdata.output



class TestDebug(unittest.TestCase):


    def testDebug(self):
        """
        debug() works as we expect
        """
        orig_logging = fetchdata.output.logging.debug
        s = StringIO()
        fetchdata.output.logging.debug = s.write
        fetchdata.output.debug_level = 0
        debug("Nothing should happen", level=1)
        self.assertEqual('', s.getvalue())
        fetchdata.output.debug_level = 2
        debug("Something should happen", level=1)
        self.assertNotEqual('', s.getvalue())


        fetchdata.output.logging.debug = orig_logging



class TestColors(unittest.TestCase):


    def testTermcolorTrue(self):
        """
        termcolor=True results in terminal output
        """
        c = Colors(termcolor=True)
        self.assertTrue(c.termcolor)
        self.assertTrue(len(c.bold("")) > 0)


    def testTermcolorFalse(self):
        """
        termcolor=False results in no terminal output
        """
        c = Colors(termcolor=False)
        self.assertFalse(c.termcolor)
        self.assertFalse(len(c.bold("")) > 0)


    def testTermcolorAuto(self):
        """
        termcolor=None causes termcolor autodetected and set to True or False
        """
        c = Colors()
        self.assertTrue(c.termcolor in [True, False])


    def testUp(self):
        """
        calling up gives us a non-blank string
        """
        c = Colors()
        up = c.up()
        self.assertEqual(type(up), str)
        self.assertNotEqual(up, '')


    def testTermstyleColorsDoNotCrash(self):
        """
        termstyle-based colors don't crash and output something
        """
        c = Colors(termcolor=True)
        for func in [c.bold, c.blue, c.fetchdata, c.red, c.yellow, c.passing,
                c.failing, c.error, c.skipped, c.unexpectedSuccess,
                c.expectedFailure, c.moduleName]:
            self.assertTrue(len(func("")) > 0)
        # c.className is a special case
        c.className("")


class TestfetchdataStream(unittest.TestCase):


    def testFormatText(self):
        """
        formatText returns the input text by default
        """
        s = StringIO()
        gs = fetchdataStream(s)
        msg = u"Unindented line.\n  Indented.\n    Double-indented.\n\n\n"
        self.assertEqual(gs.formatText(msg), str(msg))


    def testBadStringType(self):
        """
        passing the wrong stream type to fetchdataStream gets auto-converted
        """
        s = StringIO()
        gs = fetchdataStream(s)
        msg = "some string"
        if sys.version_info[0] == 3: # pragma: no cover
            bad_str = bytes(msg, 'utf-8')
        else: # pragma: no cover
            bad_str = str(msg)
        gs.write(bad_str)
        self.assertEqual(s.getvalue(), msg)
