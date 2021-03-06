from __future__ import unicode_literals
from argparse import Namespace
try:
    from io import StringIO
except:
    from StringIO import StringIO
import sys
import unittest
try:
    from unittest.mock import MagicMock, patch
except:
    from mock import MagicMock, patch

from fetchdata import djangorunner
from fetchdata.config import mergeConfig


class TestDjangoMissing(unittest.TestCase):


    def test_importError(self):
        self.assertRaises(ImportError, djangorunner.django_missing)




class TestDjangoRunner(unittest.TestCase):


    def setUp(self):
        try:
            djangorunner.DjangoRunner()
        except ImportError:
            raise unittest.SkipTest("Django is not installed")
        saved_stdout = sys.stdout
        self.stream = StringIO()
        sys.stdout = self.stream
        self.addCleanup(setattr, sys, 'stdout', saved_stdout)


    def test_run_testsWithLabel(self):
        dr = djangorunner.DjangoRunner()
        dr.setup_test_environment    = MagicMock()
        dr.setup_databases           = MagicMock()
        dr.teardown_databases        = MagicMock()
        dr.teardown_test_environment = MagicMock()

        dr.run_tests(('fetchdata.test.test_version',), testing=True)

        self.assertIn('OK', self.stream.getvalue())


    def test_run_testsWithoutLabel(self):
        """
        Not passing in a label causes the targets to be ['.']
        """
        dr = djangorunner.DjangoRunner()
        dr.setup_test_environment    = MagicMock()
        dr.setup_databases           = MagicMock()
        dr.teardown_databases        = MagicMock()
        dr.teardown_test_environment = MagicMock()

        saved_loadTargets = djangorunner.loadTargets
        djangorunner.loadTargets = MagicMock()
        self.addCleanup(setattr, djangorunner, 'loadTargets', saved_loadTargets)

        dr.run_tests((), testing=True)
        djangorunner.loadTargets.assert_called_with(['.'])
        self.assertIn('No Tests Found', self.stream.getvalue())


    def test_run_testsWithBadInput(self):
        """
        Bad input causes a ValueError to be raised
        """
        dr = djangorunner.DjangoRunner()
        dr.setup_test_environment    = MagicMock()
        dr.setup_databases           = MagicMock()

        self.assertRaises(ValueError, dr.run_tests, None, True)


    @patch('fetchdata.djangorunner.fetchdataTestSuite')
    @patch('fetchdata.djangorunner.run')
    @patch('fetchdata.djangorunner.loadTargets')
    def test_run_noTests(self, mock_loadTargets, mock_run, mock_fetchdataTestSuite):
        """
        If no tests are found, we create an empty test suite and run it.
        """
        dr = djangorunner.DjangoRunner()

        dr.setup_test_environment        = MagicMock()
        dr.setup_databases               = MagicMock()
        dr.teardown_databases            = MagicMock()
        dr.teardown_test_environment     = MagicMock()
        mock_loadTargets.return_value    = None
        mock_fetchdataTestSuite.return_value = 123

        dr.run_tests((), testing=True)

        self.assertEqual(mock_run.call_args[0][0], 123)

    @patch('fetchdata.djangorunner.mergeConfig')
    @patch('fetchdata.djangorunner.fetchdataTestSuite')
    @patch('fetchdata.djangorunner.run')
    @patch('fetchdata.djangorunner.loadTargets')
    def test_run_coverage(self, mock_loadTargets, mock_run, mock_fetchdataTestSuite, mock_mergeConfig):
        """
        If no tests are found, we create an empty test suite and run it.
        """
        args = mergeConfig(Namespace())
        args.run_coverage = True
        args.cov = MagicMock()
        mock_mergeConfig.return_value = args
        dr = djangorunner.DjangoRunner()

        dr.setup_test_environment        = MagicMock()
        dr.setup_databases               = MagicMock()
        dr.teardown_databases            = MagicMock()
        dr.teardown_test_environment     = MagicMock()
        mock_loadTargets.return_value    = None
        mock_fetchdataTestSuite.return_value = 123

        dr.run_tests((), testing=True)

        self.assertEqual(mock_run.call_args[0][0], 123)
