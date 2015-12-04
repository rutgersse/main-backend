from __future__ import unicode_literals
from __future__ import print_function

import copy
import unittest
try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock

from hma.suite import hmaTestSuite
from hma.config import default_args



class TesthmaTestSuite(unittest.TestCase):

    def test_empty(self):
        """
        An empty suite can be instantiated.
        """
        hmaTestSuite()


    def test_defaultArgs(self):
        """
        Passing in default arguments causes attributes to be set.
        """
        gts = hmaTestSuite(args=default_args)
        self.assertEqual(gts.allow_stdout, default_args.allow_stdout)


    def test_shouldStop(self):
        """
        When result.shouldStop == True, the suite should exit early.
        """
        mock_test = MagicMock()
        gts = hmaTestSuite(args=default_args)
        gts._tests = (mock_test,)
        mock_result = MagicMock()
        mock_result.shouldStop = True
        gts.run(mock_result)

    def test_failedSetup(self):
        """
        When class setup fails, we skip to the next test.
        """
        mock_test = MagicMock()
        mock_test.__iter__.side_effect = TypeError
        gts = hmaTestSuite(args=default_args)
        gts._tests = (mock_test,)
        mock_result = MagicMock()
        mock_result._moduleSetUpFailed = True
        mock_result.shouldStop = False
        gts.run(mock_result)


    def test_addTest_testPattern(self):
        """
        Setting test_pattern will cause a test to be filtered.
        """
        mock_test = MagicMock()
        mock_test._testMethodName = 'test_hello'
        mock_test2 = MagicMock()
        mock_test2._testMethodName = 'test_goodbye'
        args = copy.deepcopy(default_args)
        args.test_pattern = '_good*'
        gts = hmaTestSuite(args=args)
        gts.addTest(mock_test)
        self.assertEqual(gts._tests, [])
        gts.addTest(mock_test2)
        self.assertEqual(gts._tests, [mock_test2])


    def test_allow_stdout(self):
        """
        The allow_stdout setting should not get ignored.
        """
        class Object(object):
            pass
        args = Object()
        args.allow_stdout = True
        gts = hmaTestSuite(args=args)
        self.assertEqual(gts.allow_stdout, True)

