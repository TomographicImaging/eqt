import sys

from PySide2 import QtWidgets

from eqt.ui import UIFormFactory


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

        dialog = QtWidgets.QDialog(parent=self)
        bb = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                                        | QtWidgets.QDialogButtonBox.Cancel)

        bb.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(lambda: self.accepted())
        bb.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(lambda: self.rejected())
        self.buttonBox = bb

        # create a form layout widget
        fw = UIFormFactory.getQWidget(parent=self)

        # ## Example on how to add elements to the form

        # add title
        qlabel = QtWidgets.QLabel(fw.groupBox)
        qlabel.setText("Form Widget")
        fw.addTitle(qlabel, 'title')

        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(fw.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(fw.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        fw.addWidget(qwidget, qlabel, 'input1')

        # add separator
        fw.addSeparator('separator_1_2')

        # add input 2 as QComboBox
        qlabel = "Input2: "
        qwidget = QtWidgets.QComboBox(fw.groupBox)
        qwidget.addItem("option 1")
        qwidget.addItem("option 2")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        # finally add to the form widget
        fw.addWidget(qwidget, qlabel, 'input2')

        # Example of using 'getWidget':
        fw.getWidget('input2', 'label').setText("Input 2: ")

        # add the button box to the vertical layout, but outside the
        # form layout
        fw.uiElements['verticalLayout'].addWidget(bb)
        dialog.setLayout(fw.uiElements['verticalLayout'])

        # store a reference
        self.fw = fw
        self.dialog = dialog

        dialog.exec()

    def accepted(self):
        print("accepted")
        print(self.fw.widgets['input1_field'].text())
        print(self.fw.widgets['input2_field'].currentText())

        self.dialog.close()

    def rejected(self):
        print("rejected")
        self.dialog.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
