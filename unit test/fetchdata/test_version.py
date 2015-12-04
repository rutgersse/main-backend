from __future__ import unicode_literals
import unittest

from fetchdata.version import __version__, pretty_version
import fetchdata.version



class TestVersion(unittest.TestCase):

    def test_versionType(self):
        """
        __version__ is a unicode string
        """
        self.assertEqual(type(__version__), type(''))


    def test_versionSet(self):
        """
        __version__ is not blank
        """
        self.assertTrue(len(__version__) > 0)


    def test_pretty_version(self):
        """
        pretty_version() has the content we expect
        """
        pv = pretty_version()
        self.assertTrue('fetchdata' in pv)
        self.assertTrue('Python' in pv)
        if fetchdata.version.coverage:
            self.assertTrue('Coverage' in pv)

