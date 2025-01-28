import sys

from qtpy import QtWidgets

from eqt.ui import FormDialog, UIFormWidget, UISliderWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        '''Creates a QMainWindow and adds a FormDockWidget, a FormDialog, and a QPushButton.
        Opening the FormDockWidget will show the form in a separate window, and clicking
        on the QPushButton will also display a form separately.
        The form will initially show three widget labels and fields:
        a QLineEdit, a spanning QLabel, a QComboBox, and a QPushButton.
        Clicking the QPushButton will add additional widgets:
        a QLineEdit, a spanning QPushButton, and a UISlider.

        Opening the FormDialog shows an additional QPushButton, which will insert a
        widget in the FormDialog's vertical layout.
        '''
        QtWidgets.QMainWindow.__init__(self, parent)

        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Dock Widget Insert Widget Example')
        self.addWidgetsToExampleForm(dock)

        form_dialog_button = QtWidgets.QPushButton(self)
        form_dialog_button.setText("Open FormDialog")
        form_dialog_button.clicked.connect(self.openFormDialog)

        self.dialog = FormDialog(parent=self, title='Form Dialog Insert Widget Example')
        self.addWidgetsToExampleForm(self.dialog)

        insert_vertical_button = QtWidgets.QPushButton()
        insert_vertical_button.setText("Insert widget in vertical layout")
        self.dialog.addSpanningWidget(insert_vertical_button, 'qbutton insert vertical')
        insert_vertical_button.clicked.connect(lambda: self.insert_vertical())

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(dock)
        layout.addWidget(form_dialog_button)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        print('\nDictionary of widgets before insertion in the form layout:')
        for widget in dock.getWidgets():
            print(widget, dock.getWidgets()[widget])

        self.dialog.onCancel = self.onCancel
        self.show()

    def openFormDialog(self):
        self.dialog.open()

    def addWidgetsToExampleForm(self, form):
        '''Creates the 'initial' widgets, i.e. a QLineEdit, a spanning QLabel and
        a QComboBox. Adds them to the FormDialog.
        Also adds a QPushButton that, when clicked, inserts additional widgets into
        the FormDialog.
        '''
        form.addWidget(QtWidgets.QLineEdit(), "Initial QLineEdit Row 0:",
                       'initial qlineedit row 0')

        form.addSpanningWidget(QtWidgets.QLabel("Initial Spanning QLabel Row 1"),
                               'initial spanning qlabel row 1')

        qwidget = QtWidgets.QComboBox(form)
        qwidget.addItem("0")
        qwidget.addItem("1")
        form.addWidget(qwidget, "Initial QComboBox Row 2:", 'initial qcombobox row 2')

        buttoninsert = QtWidgets.QPushButton()
        buttoninsert.setText("Insert widgets")
        form.addSpanningWidget(buttoninsert, 'qbutton insert widgets')
        buttoninsert.clicked.connect(lambda: self.insert_form(form, buttoninsert))

    def insert_vertical(self):
        '''Inserts a QPushButton into the vertical layout. The widget is not added to
        the dictionary of FormDialog widgets. Also sets the 'enabled' value of the button
        that calls this method to 'False'.
        '''
        self.dialog.insertWidgetToVerticalLayout(
            1, QtWidgets.QPushButton("Inserted widget in vertical layout"))
        print(
            "\nThe dictionary of widgets does not change after insertion in the vertical layout.")
        self.dialog.getWidget('qbutton insert vertical').setEnabled(False)

    def insert_form(self, form, button):
        '''Inserts additional widgets into the specified rows of the FormDialog: a QLineEdit,
        a spanning QPushButton, and a UISlider. Prints the dictionary containing all widgets
        in the FormDialog layout.
        '''
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Inserted Widget Row 0:")
        qwidget = QtWidgets.QLineEdit(form)
        form.insertWidget(0, 'inserted qlineedit row 0', qwidget, qlabel)

        buttonspanning = QtWidgets.QPushButton(self)
        buttonspanning.setText("Inserted Spanning Widget Row 2")
        form.insertWidget(2, 'inserted spanning qpushbutton row 2', buttonspanning)

        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Inserted Widget Row 4:")
        uislider = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5, decimals=10,
                                                 number_of_steps=10, number_of_ticks=10)
        form.insertWidget(4, 'inserted uislider row 4', uislider, qlabel)

        print('\nDictionary of widgets after insertion in the form layout:')
        for widget in form.getWidgets():
            print(widget, form.getWidgets()[widget])

        button.setEnabled(False)

    def onCancel(self):
        '''Defines the behaviour of the 'cancel' button.
        If the button is pressed and the FormDialog widget states have not been saved, it checks
        whether the 'insert widget' buttons have been pressed. If they have, the method removes
        the inserted widgets from the FormDialog and the dictionary of FormDialog widgets.
        Otherwise, it only removes the widgets from the FormDialog.
        '''
        if bool(self.dialog.formWidget.widget_states) is False:
            if self.dialog.getWidget('qbutton insert vertical').isEnabled() is False:
                self.dialog.removeWidgetFromVerticalLayout(
                    self.dialog.getWidgetFromVerticalLayout(1))
            if self.dialog.getWidget('qbutton insert widgets').isEnabled() is False:
                self.dialog.formWidget._popWidget(self.dialog.formWidget.default_widget_states,
                                                  'inserted qlineedit row 0')
                self.dialog.formWidget._popWidget(self.dialog.formWidget.default_widget_states,
                                                  'inserted spanning qpushbutton row 2')
                self.dialog.formWidget._popWidget(self.dialog.formWidget.default_widget_states,
                                                  'inserted uislider row 4')
                self.dialog.formWidget.removeWidget('inserted qlineedit row 0')
                self.dialog.formWidget.removeWidget('inserted spanning qpushbutton row 2')
                self.dialog.formWidget.removeWidget('inserted uislider row 4')
        else:
            if self.dialog.getWidget(
                    'qbutton insert vertical').isEnabled() != self.dialog.getSavedWidgetStates(
                    )['qbutton insert vertical_field']['enabled'] is True:
                self.dialog.removeWidgetFromVerticalLayout(
                    self.dialog.getWidgetFromVerticalLayout(1))
            if self.dialog.getWidget(
                    'qbutton insert widgets').isEnabled() != self.dialog.getSavedWidgetStates(
                    )['qbutton insert widgets_field']['enabled'] is True:
                self.dialog.formWidget.removeWidget('inserted qlineedit row 0')
                self.dialog.formWidget.removeWidget('inserted spanning qpushbutton row 2')
                self.dialog.formWidget.removeWidget('inserted uislider row 4')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
