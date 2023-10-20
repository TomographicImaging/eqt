import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with form layout")

        pb.clicked.connect(lambda: self.executedialog())
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)
        self.dialog = FormDialog(parent=self, title='Example')

        self.openFormDialog()
        self.show()

    def openFormDialog(self):
        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(self.dialog.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(self.dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        self.dialog.addSpanningWidget(QtWidgets.QLabel("Input Values: "), 'input_title')
        self.dialog.addWidget(qwidget, qlabel, 'input1')

        # add input 2 as QComboBox
        qlabel = QtWidgets.QLabel(self.dialog.groupBox)
        qlabel.setText("Input 2: ")
        qwidget = QtWidgets.QComboBox(self.dialog.groupBox)
        qwidget.addItem("option 1")
        qwidget.addItem("option 2")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        self.dialog.addWidget(qwidget, qlabel, 'input2')
        self.dialog.addWidget(QtWidgets.QLabel("Example Vertical Layout Text"), layout="vertical")

        # Example of using 'getWidget':
        self.dialog.getWidget('input2').setCurrentIndex(1)

        #redefine the onOk and onCancel functions
        self.dialog.onOk = self.accepted
        self.dialog.onCancel = self.rejected

    #open dialog function when the parent button is clicked
    def executedialog(self):
        self.dialog.open()

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
