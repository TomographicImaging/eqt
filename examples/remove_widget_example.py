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
        dialog = FormDialog(parent=self, title='Example')
        
        # Example on how to add elements to the FormDialog
        
        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        dialog.addSpanningWidget(QtWidgets.QLabel("Input Values: "), 'input_title')
        dialog.addWidget(qwidget, qlabel, 'input1')
        dialog.Ok.clicked.connect(lambda: self.accepted())


        # add a button to remove widget
        # button box
        buttonremove = QtWidgets.QPushButton(self)
        buttonremove.setText("remove Widget")
        buttonremove.clicked.connect(lambda: self.remove(qwidget,qlabel))
        # add button box to the UI
        buttonBox = buttonremove
        dialog.formWidget.uiElements['verticalLayout'].addWidget(buttonremove)
        #dialog.removeWidget(qwidget, qlabel)
        #qwidget.show()
        #qlabel.show()
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
        dialog.addWidget(QtWidgets.QLabel("Example Vertical Layout Text"), layout="vertical")

        # Example of using 'getWidget':
        dialog.getWidget('input2').setCurrentIndex(1)

        buttonremove.deleteLater()
        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected
        dialog.exec()


    def remove(self,qwidget, qlabel=None):
        print("Remove")
        self.dialog.removeWidget(qwidget, qlabel)

    def accepted(self):
        print("accepted")
        print(self.dialog.widgets['input1_field'].text())
        print(self.dialog.widgets['input2_field'].currentText())
        self.dialog.close()

    def rejected(self):
        print("rejected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
