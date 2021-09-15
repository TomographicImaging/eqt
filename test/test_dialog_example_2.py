from PySide2 import QtCore, QtWidgets, QtTest
from PySide2.QtTest import QTest
from PySide2.QtCore import Qt
import glob
import sys
import os
from eqt.ui import UIFormFactory, FormDialog
import unittest


class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with form layout")
        pb.clicked.connect(lambda: self.openFormDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)
        self.push_button = pb

        self.setCentralWidget(widg)

        self.show()

    def openFormDialog(self):

        dialog = FormDialog(parent=self, title='Example')
        dialog.Ok.clicked.connect(lambda: self.accepted())
        dialog.Cancel.clicked.connect(lambda: self.rejected())

        # Example on how to add elements to the
        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        dialog.addWidget(qwidget, qlabel, 'input1', layout='form')

        # add input 2 as QComboBox
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Input 2: ")
        qwidget = QtWidgets.QComboBox(dialog.groupBox)
        qwidget.addItem("option 1")
        qwidget.addItem("option 2")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        # finally add to the form widget
        dialog.addWidget(qwidget, qlabel, 'input2')

        # store a reference
        self.dialog = dialog

        dialog.exec()

    def accepted(self):
        print("accepted")
        print(self.dialog.widgets['input1_field'].text())
        print(self.dialog.widgets['input2_field'].currentText())

        self.dialog.close()

    def rejected(self):
        print("rejected")
        self.dialog.close()


_instance = None


class DialogTest(unittest.TestCase):
    '''Test the margarita mixer GUI'''

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

    def tearDown(self):
        del self.app
        super(DialogTest, self).tearDown()

    def test_close(self):
        self.window.close()
        self.assertTrue(True)

    def test_openclose_dialog(self):
        QTest.mouseClick(self.window.push_button, Qt.LeftButton)
        dialog = self.window.dialog
        print(dialog)
        dialog.close()

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


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
