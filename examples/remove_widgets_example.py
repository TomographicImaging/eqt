import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UIFormWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create a FormDockWidget
        dock = UIFormWidget.FormDockWidget(parent=self, title='Example remove widget')
        self.addWidgetsToExampleForm(dock)

        # add a button to dock to remove user selected widget
        buttonuser = QtWidgets.QPushButton(dock)
        buttonuser.setText("Remove user selected widget")
        dock.addSpanningWidget(buttonuser, 'Button Remove User')
        buttonuser.clicked.connect(lambda: self.remove(dock, buttonuser))

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
        dialog = FormDialog(parent=self, title='Example remove widget')
        dialog.Ok.clicked.connect(lambda: self.remove(dialog, dialog.Ok))
        self.addWidgetsToExampleForm(dialog)
        buttonremovevertical = QtWidgets.QPushButton()
        buttonremovevertical.setText("Remove widget in vertical layout")
        dialog.addSpanningWidget(buttonremovevertical, 'Button remove vertical')
        vertical_button = QtWidgets.QPushButton("Widget in vertical layout")
        buttonremovevertical.clicked.connect(lambda: self.remove_vertical(vertical_button))
        dialog.insertWidgetToVerticalLayout(1, vertical_button)
        dialog.addSpanningWidget(
            QtWidgets.QLabel(
                "Press `Ok` to remove the user selected widget and `Cancel` to close the dialog:"),
            'ok_cancel_instructions')

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected
        # redefine `onOk`` so it does not close the dialog.
        self.dialog._onOk = self._onOkRedefined

        # print dictionary of all widgets in dialog
        print("\nDictionary of widgets in Form Dialog:\n" + str(self.dialog.getWidgets()))

        dialog.open()

    def _onOkRedefined(self):
        '''Saves the widget states.'''
        self.dialog.saveAllWidgetStates()

    def addWidgetsToExampleForm(self, form):

        # add widget 1 as QLineEdit
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 1: ")
        qwidget = QtWidgets.QLineEdit(form)
        qwidget.setClearButtonEnabled(True)
        form.addWidget(qwidget, qlabel, 'Widget 1')

        # add widget 2 as QLineEdit
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 2: ")
        qwidget = QtWidgets.QLineEdit(form)
        qwidget.setClearButtonEnabled(True)
        form.addWidget(qwidget, qlabel, 'Widget 2')

        # add widget 3 as QLineEdit
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 3: ")
        qwidget = QtWidgets.QLineEdit(form)
        qwidget.setClearButtonEnabled(True)
        form.addWidget(qwidget, qlabel, 'Widget 3')

        # add input as QComboBox
        form.addSpanningWidget(QtWidgets.QLabel("Pick the widget you want to remove:"),
                               'input_title')
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("User input: ")
        qwidget = QtWidgets.QComboBox(form)
        qwidget.addItem("Widget 2")
        qwidget.addItem("Widget 3")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        form.addWidget(qwidget, qlabel, 'userinput')

        # add a button to remove widget 1
        button1 = QtWidgets.QPushButton(form)
        button1.setText("Remove widget 1")
        form.addSpanningWidget(button1, 'Button Remove w1')
        button1.clicked.connect(lambda: self.remove(form, button1, 'Widget 1'))

        # add a button to remove spanning widget
        buttonspanning = QtWidgets.QPushButton(form)
        buttonspanning.setText("Remove spanning widget")
        form.addSpanningWidget(buttonspanning, 'Button Remove Spanning')
        buttonspanning.clicked.connect(lambda: self.remove(form, buttonspanning, 'input_title'))

    def remove_vertical(self, button):
        widget = self.dialog.removeWidgetFromVerticalLayout(button)
        print(f'\nRemoved widget in the vertical layout is {widget}.')
        self.dialog.getWidget('Button remove vertical').setEnabled(False)

    def rejected(self):
        print("\nDialog closed.")

    def remove(self, form, button, userselection=False):
        if userselection is False:
            userselection = form.getWidget('userinput').currentText()
            form.getWidget('userinput').removeItem(form.getWidget('userinput').currentIndex())

        widget = form.removeWidget(userselection)
        print(f'\nRemove {userselection} returning {widget}.')
        if form.getWidget('userinput').currentIndex() == -1:
            button.setEnabled(False)
        if button == form.getWidget('Button Remove w1') or button == form.getWidget(
                'Button Remove Spanning'):
            button.setEnabled(False)

        print("\nDictionary of widgets after deletion of " + userselection + ":\n" +
              str(form.getWidgets()))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
