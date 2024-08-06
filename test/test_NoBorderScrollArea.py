import unittest

from PySide2.QtWidgets import QHBoxLayout, QPushButton, QWidget

from eqt.ui.NoBorderScrollArea import NoBorderScrollArea


class TestNoBorderScrollArea(unittest.TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     '''If not present already, creates a QApplication.'''
    #     if not QApplication.instance():
    #         app = QApplication([])
    #     else:
    #         app = QApplication.instance()

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
