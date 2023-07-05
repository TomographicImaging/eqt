import unittest
import os

# skip test of UI imports on GitHub actions
if os.environ.get('CONDA_BUILD', '0') != '1':
    from dialog_example_2_test import MainUI, DialogTest

class TestModuleBase(unittest.TestCase):
    pass
