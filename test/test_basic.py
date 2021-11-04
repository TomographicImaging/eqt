import unittest
import os

# skip test of UI imports on GitHub actions
if os.environ.get('CONDA_BUILD', '0') == '0':
    from dialog_example_2_test import MainUI, DialogTest

class TestModuleBase(unittest.TestCase):
    def test_version(self):
        try:
            from eqt import version as dversion
            a = dversion.version
            print ("version", a)
            self.assertTrue(isinstance(a, str))
        except ImportError as ie:
            self.assertFalse(True, str(ie))
