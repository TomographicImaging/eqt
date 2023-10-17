import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog


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

        self.setCentralWidget(widg)

        self.show()

    def openFormDialog(self):
        dialog = FormDialog(parent=self, title='Example remove widget')

        dialog.Ok.clicked.connect(lambda: self.remove())

        # add widget 1 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Widget 1: ")
        qwidget = QtWidgets.QLineEdit(dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        dialog.addWidget(qwidget, qlabel, 'Widget 1')

        # add widget 2 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Widget 2: ")
        qwidget = QtWidgets.QLineEdit(dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        dialog.addWidget(qwidget, qlabel, 'Widget 2')

        # add widget 3 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Widget 3: ")
        qwidget = QtWidgets.QLineEdit(dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        dialog.addWidget(qwidget, qlabel, 'Widget 3')

        # add input as QComboBox
        dialog.addSpanningWidget(
            QtWidgets.QLabel("Pick the widget you want to remove then press ok: "), 'input_title')
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("User input: ")
        qwidget = QtWidgets.QComboBox(dialog.groupBox)
        qwidget.addItem("Widget 2")
        qwidget.addItem("Widget 3")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        dialog.addWidget(qwidget, qlabel, 'userinput')

        # add a button to remove widget 1
        buttonremove = QtWidgets.QPushButton(dialog.groupBox)
        buttonremove.setText("Remove widget 1")
        dialog.addSpanningWidget(buttonremove, 'Button Remove')
        buttonremove.clicked.connect(lambda: self.remove('Widget 1'))

        # add a button to remove spanning widget
        buttonremove = QtWidgets.QPushButton(dialog.groupBox)
        buttonremove.setText("Remove spanning widget")
        dialog.addSpanningWidget(buttonremove, 'Button Remove Spanning')
        buttonremove.clicked.connect(lambda: self.remove('input_title'))

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected

        # print dictionary of all widgets
        print("Dictionary of widgets:\n" + str(self.dialog.getWidgets()))
        dialog.exec()

    def remove(self, userselection=False):
        if userselection is False:
            userselection = self.dialog.getWidget('userinput').currentText()
        print("Remove " + userselection)
        self.dialog.removeWidget(userselection)
        print("Dictionary of widgets after deletion of " + userselection + ":\n" +
              str(self.dialog.getWidgets()))

    def rejected(self):
        print("Close the dialog")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
