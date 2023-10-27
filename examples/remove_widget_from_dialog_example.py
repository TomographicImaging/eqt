import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog

from eqt.ui import UIFormWidget

import utilitiesForExamples as utex


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        #create a FormDockWidget
        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Example remove widget')
        utex.addWidgetsToExample(self,dock)

        # add a button to remove user selected widget
        buttonremove = QtWidgets.QPushButton(dock)
        buttonremove.setText("Remove user selected widget")
        dock.addSpanningWidget(buttonremove, 'Button Remove User')
        buttonremove.clicked.connect(lambda: self.remove(dock))

        #create button for Form Dialog
        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Form Dialog")
        pb.clicked.connect(lambda: self.openFormDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        layout.addWidget(dock)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        self.show()

    def openFormDialog(self):
        dialog = FormDialog(parent=self, title='Example remove widget')

        dialog.Ok.clicked.connect(lambda: self.remove(dialog))

        utex.addWidgetsToExample(self,dialog)
        

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected

        # print dictionary of all widgets
        print("Dictionary of widgets:\n" + str(self.dialog.getWidgets()))
        dialog.open()

    def rejected(self):
        print("Close the dialog")


    def remove(self, form, userselection=False):
        if userselection is False:
            userselection = form.getWidget('userinput').currentText()
        print("Remove " + userselection)
        form.removeWidget(userselection)
        print("Dictionary of widgets after deletion of " + userselection + ":\n" +
                str(form.getWidgets()))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
