import sys

from PySide2 import QtWidgets

from eqt.ui import UIFormFactory, UIMultiStepFactory


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with MultiStep widget")
        pb.clicked.connect(lambda: self.openMultiStepDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        self.show()

    def openMultiStepDialog(self):

        dialog = QtWidgets.QDialog(parent=self)
        bb = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                                        | QtWidgets.QDialogButtonBox.Cancel)

        bb.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(lambda: self.accepted())
        bb.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(lambda: self.rejected())
        self.buttonBox = bb

        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setContentsMargins(10, 10, 10, 10)

        # Add vertical layout to main widget (self)
        dialog.setLayout(verticalLayout)

        # create a form layout widget
        fw1 = UIFormFactory.getQWidget(parent=self)

        # ## Example on how to add elements to the form

        # add title
        qlabel = QtWidgets.QLabel(fw1.groupBox)
        qlabel.setText("Form Widget 1")
        fw1.addTitle(qlabel, 'title')

        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(fw1.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(fw1.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        fw1.addWidget(qwidget, qlabel, 'input1')

        # add separator
        fw1.addSeparator('separator_1_2')

        # add input 2 as QComboBox
        qlabel = "Input 2: "
        qwidget = QtWidgets.QComboBox(fw1.groupBox)
        qwidget.addItem("option 1")
        qwidget.addItem("option 2")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        # finally add to the form widget
        fw1.addWidget(qwidget, qlabel, 'input2')

        # create a 2nd form layout widget
        fw2 = UIFormFactory.getQWidget(parent=self)

        # ## Example on how to add elements to the form

        # add title
        qlabel = QtWidgets.QLabel(fw2.groupBox)
        qlabel.setText("Form Widget 2")
        fw2.addTitle(qlabel, 'title')

        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(fw2.groupBox)
        qlabel.setText("Input 3: ")
        qwidget = QtWidgets.QLineEdit(fw2.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        fw2.addWidget(qwidget, qlabel, 'input3')

        multistep_widget = UIMultiStepFactory.getQWidget(parent=self)
        multistep_widget.addStepWidget(fw1, 'fw1')
        multistep_widget.addStepWidget(fw2, 'fw2')

        verticalLayout.addWidget(multistep_widget)
        verticalLayout.addWidget(bb)

        # store a reference
        self.fw1 = fw1
        self.fw2 = fw2
        self.dialog = dialog

        dialog.exec()

    def accepted(self):
        print("accepted")
        print(self.fw1.widgets['input1_field'].text())
        print(self.fw1.widgets['input2_field'].currentText())
        print(self.fw2.widgets['input3_field'].text())

        self.dialog.close()

    def rejected(self):
        print("rejected")
        self.dialog.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
