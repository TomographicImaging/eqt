import os

from PySide2 import QtWidgets
from pytest import skip

from eqt.ui import FormDialog

is_ci = any(os.getenv(var, '0').lower() in ('1', 'true') for var in ('CONDA_BUILD', 'CI'))

if is_ci:

    def skip_ci(_):
        def inner(*_, **__):
            skip("Running in CI (no GUI)")

        return inner
else:

    def skip_ci(fn):
        return fn


@skip_ci
def test_import():
    from dialog_example_2_test import DialogTest, MainUI # NOQA:F401 isort:skip


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
