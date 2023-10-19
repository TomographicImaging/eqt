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
        # Example on how to add elements to the FormDialog
        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(self.dialog.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(self.dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
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
        # finally add to the form widget
        self.dialog.addWidget(qwidget, qlabel, 'input2')
        self.dialog.addWidget(QtWidgets.QLabel("Example Vertical Layout Text"), layout="vertical")

        # Example of using 'getWidget':
        self.dialog.getWidget('input2').setCurrentIndex(1)

        # store a reference
        #self.dialog = dialog
        self.dialog.onOk = self.accepted
        self.dialog.onCancel = self.rejected

        #self.dialog.restoreAllSavedWidgetStates()
        if hasattr(self.dialog, 'widget_states'):
            print("There are states")
            print(self.dialog.widget_states)
    
    def executedialog(self):
        self.dialog.restoreAllSavedWidgetStates()
        self.dialog.exec()

    def accepted(self):
        self.dialog.widget_states = self.dialog.saveAllWidgetStates()    
        print("accepted")
        print(self.dialog.widgets['input1_field'].text())
        print(self.dialog.widgets['input2_field'].currentText())
        #print(self.widget_states)
        print(self.dialog.widget_states)
        self.dialog.close()

    def rejected(self):
        print("rejected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
