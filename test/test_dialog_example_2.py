from PySide2 import QtWidgets
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt
import glob
import sys
import os
import unittest

# skip the tests on GitHub actions
if os.environ.get('CONDA_BUILD', 0) == 1:
    from common import MainUI
    skip_as_conda_build = True

else:
    skip_as_conda_build = False

print ("skip_as_conda_build is set to ", skip_as_conda_build)




_instance = None


class DialogTest(unittest.TestCase):
    '''Test the margarita mixer GUI'''

    @unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
    def setUp(self):
        '''Create the GUI'''
        super(DialogTest, self).setUp()

        global _instance
        if _instance is None:
            _instance = QtWidgets.QApplication(sys.argv)

        self.app = _instance
        window = MainUI()
        self.app = _instance
        self.window = window
        # QTest.mouseClick(self.window.push_button, Qt.LeftButton)
        # self.dialog = window.dialog

    @unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
    def tearDown(self):
        del self.app
        super(DialogTest, self).tearDown()

    @unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
    def test_close(self):
        self.window.close()
        self.assertTrue(True)

    @unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
    def test_openclose_dialog(self):
        QTest.mouseClick(self.window.push_button, Qt.LeftButton)
        dialog = self.window.dialog
        print(dialog)
        dialog.close()

    @unittest.skipUnless(skip_as_conda_build, "On conda builds do not do any test with interfaces")
    def stest_defaults(self):
        '''Test the GUI in its default state'''

        self.dialog = self.window.dialog
        print("test1")
        self.assertEqual(self.window.dialog.widgets['input1_field'].text(), '')
        print("test2")
        self.assertEqual(
            self.window.dialog.widgets['input2_field'].currentIndex(), 0)
        print("click")
        print(self.window.dialog.Ok, self.window.dialog.Cancel)
        QTest.mouseClick(self.window.push_button, Qt.LeftButton)
