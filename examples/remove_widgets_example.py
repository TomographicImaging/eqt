import sys

from qtpy import QtWidgets

from eqt.ui import FormDialog, UIFormWidget, UISliderWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        '''Creates a QMainWindow and adds a FormDockWidget, a FormDialog, and a QPushButton.
        Opening the FormDockWidget will show the form in a separate window, and clicking
        on the QPushButton will also display a form separately.

        The form will initially show six labels and fields:
            - x3 QLineEdit fields
            - a UISlider field
            - a spanning QLabel
            - a QComboBox field

        Underneath these fields are some QPushButtons that will remove the specified widgets
        when clicked. Users have the option to select a specific widget using the QComboBox field
        and clicking the 'Remove user selected widget' QPushButton.

        Opening the FormDialog displays the form with an additional QPushButton, which
        will insert a widget in the FormDialog's vertical layout.
        '''
        QtWidgets.QMainWindow.__init__(self, parent)

        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Dock Widget Remove Widget Example')
        self.addWidgetsToExampleForm(dock)

        user_button = QtWidgets.QPushButton(dock)
        user_button.setText("Remove user selected widget")
        dock.addSpanningWidget(user_button, 'qpushbutton remove user')
        user_button.clicked.connect(lambda: self.remove(dock, user_button))

        form_dialog_button = QtWidgets.QPushButton(self)
        form_dialog_button.setText("Open FormDialog")
        form_dialog_button.clicked.connect(lambda: self.openFormDialog())

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dock)
        layout.addWidget(form_dialog_button)
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        print('\nDictionary of widgets in the FormDockWidget:')
        for widget in dock.getWidgets():
            print(widget, dock.getWidgets()[widget])

        self.show()

    def openFormDialog(self):
        '''Creates a FormDialog and adds widgets to it.
        Adds a widget in the vertical layout as well as a QPushButton to remove it.
        Prints the dictionary containing all widgets in the FormDialog layout.
        '''
        self.dialog = FormDialog(parent=self, title='FormDialog Remove Widget Example')
        self.dialog.Ok.clicked.connect(lambda: self.remove(self.dialog, self.dialog.Ok))
        self.addWidgetsToExampleForm(self.dialog)

        remove_vertical_button = QtWidgets.QPushButton()
        remove_vertical_button.setText("Remove widget in vertical layout")
        self.dialog.addSpanningWidget(remove_vertical_button, 'qpushbutton remove vertical')

        vertical_button = QtWidgets.QPushButton()
        vertical_button.setText("Widget in vertical layout")
        self.dialog.insertWidgetToVerticalLayout(1, vertical_button)

        remove_vertical_button.clicked.connect(lambda: self.remove_vertical(vertical_button))

        qlabel = QtWidgets.QLabel()
        qlabel.setText(
            "Press 'OK' to remove the user selected widget, 'Cancel' to close the FormDialog")
        self.dialog.addSpanningWidget(qlabel, 'qlabel instructions')

        self.dialog.onCancel = self.rejected
        self.dialog._onOk = self._onOkRedefined

        print('\nDictionary of widgets in the FormDialog:')
        for widget in self.dialog.getWidgets():
            print(widget, self.dialog.getWidgets()[widget])

        self.dialog.saveAllWidgetStates()
        self.dialog.open()

    def _onOkRedefined(self):
        '''Saves the widget states of all widgets in the FormDialog.
        '''
        self.dialog.saveAllWidgetStates()

    def addWidgetsToExampleForm(self, form):
        '''Populates the FormDialog with widgets.
        Three QLineEdit widgets, a UISlider widget, and a QComboBox widget are added.
        The QComboBox widget allows users to select the widget they want to remove.
        Two QPushButtons are also added to remove 'Widget 1' and the spanning widget specifically.
        '''
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 1:")
        qlineedit = QtWidgets.QLineEdit(form)
        qlineedit.setClearButtonEnabled(True)
        form.addWidget(qlineedit, qlabel, 'widget 1')

        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 2:")
        qlineedit = QtWidgets.QLineEdit(form)
        qlineedit.setClearButtonEnabled(True)
        form.addWidget(qlineedit, qlabel, 'widget 2')

        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 3:")
        qlineedit = QtWidgets.QLineEdit(form)
        qlineedit.setClearButtonEnabled(True)
        form.addWidget(qlineedit, qlabel, 'widget 3')

        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget 4:")
        uislider = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5, decimals=10,
                                                 number_of_steps=10, number_of_ticks=10)
        form.addWidget(uislider, qlabel, 'widget 4')

        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Select widget to remove:")
        form.addSpanningWidget(qlabel, 'qlabel user input')

        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("User input: ")
        qcombobox = QtWidgets.QComboBox(form)
        qcombobox.addItem("widget 2")
        qcombobox.addItem("widget 3")
        qcombobox.addItem("widget 4")
        qcombobox.setCurrentIndex(0)
        qcombobox.setEnabled(True)
        form.addWidget(qcombobox, qlabel, 'qcombobox user input')

        widget_1_button = QtWidgets.QPushButton(form)
        widget_1_button.setText("Remove widget 1")
        form.addSpanningWidget(widget_1_button, 'qpushbutton remove widget 1')
        widget_1_button.clicked.connect(lambda: self.remove(form, widget_1_button, 'widget 1'))

        spanning_button = QtWidgets.QPushButton(form)
        spanning_button.setText("Remove spanning widget")
        form.addSpanningWidget(spanning_button, 'qpushbutton remove spanning')
        spanning_button.clicked.connect(
            lambda: self.remove(form, spanning_button, 'qlabel user input'))

    def remove_vertical(self, button):
        '''Removes the widget from the FormDialog's vertical layout, then
        sets the clicked QPushButton's 'enabled' value to 'False'.
        '''
        widget = self.dialog.removeWidgetFromVerticalLayout(button)
        print(f'\nRemoved widget in the vertical layout: {widget}')
        self.dialog.getWidget('qpushbutton remove vertical').setEnabled(False)

    def rejected(self):
        print("\nFormDialog closed.")

    def remove(self, form, button, user_selection=False):
        '''Removes a widget from the FormDialog.
        If the user has not specified a widget to remove in the QComboBox, the current
        selection will be removed. Otherwise, the widget specified will be deleted.
        Prints the dictionary containing all widgets in the FormDialog layout after deletion.
        '''
        if user_selection is False:
            user_selection = form.getWidget('qcombobox user input').currentText()
            form.getWidget('qcombobox user input').removeItem(
                form.getWidget('qcombobox user input').currentIndex())

        widget = form.getWidget(user_selection)
        print(f'\nRemove {user_selection} returning {widget}.')

        if isinstance(form, FormDialog):
            form.formWidget._popWidget(self.dialog.formWidget.widget_states, user_selection)
            form.formWidget.removeWidget(user_selection)
        elif isinstance(form, UIFormWidget.FormDockWidget):
            form.removeWidget(user_selection)

        if form.getWidget('qcombobox user input').currentIndex() == -1:
            button.setEnabled(False)
        if button == form.getWidget('qpushbutton remove widget 1') or button == form.getWidget(
                'qpushbutton remove spanning'):
            button.setEnabled(False)

        print(f'\nDictionary of widgets after deletion of {user_selection}:')
        for widget in form.getWidgets():
            print(widget, form.getWidgets()[widget])


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
