import sys

import utilitiesForExamples as utex
from PySide2 import QtWidgets

from eqt.ui import FormDialog


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with form layout")
        pb.clicked.connect(lambda: self.executeDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)
        self.dialog = FormDialog(parent=self, title='Example')
        self.openFormDialog()

        self.show()

    def openFormDialog(self):
        utex.addWidgetsToExample(self.dialog)
        # redefine the onOk and onCancel functions
        self.dialog.onOk = self.accepted
        self.dialog.onCancel = self.rejected

    def accepted(self):
        print("States saved")

    def rejected(self):
        print("States rejected")

    # open dialog function when the parent button is clicked
    def executeDialog(self):
        self.dialog.open()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
