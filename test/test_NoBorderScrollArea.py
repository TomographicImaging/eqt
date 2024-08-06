import unittest

from PySide2.QtWidgets import QHBoxLayout, QPushButton, QWidget

from eqt.ui.NoBorderScrollArea import NoBorderScrollArea

from . import is_ci, skip

if is_ci:
    skip("Running in CI (no GUI)", allow_module_level=True)


class TestNoBorderScrollArea(unittest.TestCase):
    def setUp(self):
        '''Initialises a NoBorderScrollArea widget and adds it to a layout.'''
        self.main_widget = QWidget()
        self.layout = QHBoxLayout(self.main_widget)
        self.scroll_area_widget = NoBorderScrollArea(QPushButton())
        self.layout.addWidget(self.scroll_area_widget)

    def test_scroll_area_creation(self):
        '''
        Tests the init method of the NoBorderScrollArea class.
        '''
        self.assertIsNotNone(self.scroll_area_widget,
                             "NoBorderScrollArea widget should be created")
