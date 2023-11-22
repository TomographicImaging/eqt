import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UIFormWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create a FormDockWidget
        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Example insert widget')
        self.addWidgetsToExampleForm(dock)
        buttoninsert = QtWidgets.QPushButton(dock)
        buttoninsert.setText("Insert widgets")
        dock.addSpanningWidget(buttoninsert, 'Button insert widgets')
        buttoninsert.clicked.connect(lambda: self.insert_form(dock, buttoninsert))

        # create button for Form Dialog
        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Form Dialog")
        pb.clicked.connect(lambda: self.openFormDialog())

        # create window layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        layout.addWidget(dock)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        # print dictionary of all widgets in dock
        print("\nDictionary of widgets in the Form Dock Widget:\n" + str(dock.getWidgets()))

        self.show()

    def openFormDialog(self):
        dialog = FormDialog(parent=self, title='Example insert widget')
        self.addWidgetsToExampleForm(dialog)
        dialog.Ok.clicked.connect(lambda: self.insert_vertical(dialog))
        dialog.Ok.clicked.connect(lambda: self.insert_form(dialog, dialog.Ok))

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected

        # print dictionary of all widgets in dialog
        print("\nDictionary of widgets in Form Dialog:\n" + str(self.dialog.getWidgets()))

        dialog.open()

    def addWidgetsToExampleForm(self, form):
        form.addWidget(QtWidgets.QLineEdit(), "Initial widget raw 0: ", 'Initial widget raw 0')
        form.addSpanningWidget(QtWidgets.QLabel("Initial widget row 1"), 'Initial widget row 1')
        # add QComboBox
        qwidget = QtWidgets.QComboBox(form)
        qwidget.addItem("0")
        qwidget.addItem("1")
        form.addWidget(qwidget, "Initial widget row 2", 'Initial widget row 2')

    def rejected(self):
        print("\nDialog closed.")

    def insert_vertical(self, form):
        form.insertWidgetToVerticalLayout(
            1, QtWidgets.QPushButton("Inserted widget in vertical layout"))
        print(
            "\nThe dictionary of widgets does not change after insertion in the vertical layout.")

    def insert_form(self, form, button):
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget inserted in row 0: ")
        qwidget = QtWidgets.QLineEdit(form)
        form.insertWidgetToFormLayout(0, 'inserted widget', qwidget, qlabel)

        buttonspanning = QtWidgets.QPushButton(self)
        buttonspanning.setText("Spanning widget inserted in row 2")
        form.insertWidgetToFormLayout(2, 'inserted spanning widget', buttonspanning)

        print('\nDictionary of widgets after insertion in the form layout:\n' +
              str(form.getWidgets()))
        button.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
