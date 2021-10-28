import unittest
import os

# skip the tests on GitHub actions
if os.environ.get('CONDA_BUILD', 0) == '1':
    skip_as_conda_build = True
else:
    skip_as_conda_build = False
    from dialog_example_2_test import MainUI, DialogTest

print ("skip_as_conda_build is set to ", skip_as_conda_build)

class TestModuleBase(unittest.TestCase):
    def test_version(self):
        try:
            from eqt import version as dversion
            a = dversion.version
            print ("version", a)
            self.assertTrue(isinstance(a, str))
        except ImportError as ie:
            self.assertFalse(True, str(ie))
