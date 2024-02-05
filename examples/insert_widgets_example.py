import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UIFormWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # dialog form
        self.dialog = FormDialog(parent=self, title='Form Dialog example insert widget')
        self.addWidgetsToExampleForm(self.dialog)
        buttoninsertvertical = QtWidgets.QPushButton()
        buttoninsertvertical.setText("Insert widget in vertical layout")
        self.dialog.addSpanningWidget(buttoninsertvertical, 'Button insert vertical')
        buttoninsertvertical.clicked.connect(lambda: self.insert_vertical())

        # create a FormDockWidget
        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Dock Widget Example insert widget')
        self.addWidgetsToExampleForm(dock)

        # create button for Form Dialog
        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Form Dialog")
        pb.clicked.connect(self.openFormDialog)

        # create window layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        layout.addWidget(dock)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        self.dialog.onCancel = self.onCancel
        self.show()

    def openFormDialog(self):
        self.dialog.open()

    def addWidgetsToExampleForm(self, form):
        form.addWidget(QtWidgets.QLineEdit(), "Initial widget row 0: ", 'Initial widget row 0')
        form.addSpanningWidget(QtWidgets.QLabel("Initial widget row 1"), 'Initial widget row 1')
        # add QComboBox
        qwidget = QtWidgets.QComboBox(form)
        qwidget.addItem("0")
        qwidget.addItem("1")
        form.addWidget(qwidget, "Initial widget row 2", 'Initial widget row 2')
        buttoninsert = QtWidgets.QPushButton()
        buttoninsert.setText("Insert widgets")
        form.addSpanningWidget(buttoninsert, 'Button insert widgets')
        buttoninsert.clicked.connect(lambda: self.insert_form(form, buttoninsert))

    def insert_vertical(self):
        self.dialog.insertWidgetToVerticalLayout(
            1, QtWidgets.QPushButton("Inserted widget in vertical layout"))
        print(
            "\nThe dictionary of widgets does not change after insertion in the vertical layout.")
        self.dialog.getWidget('Button insert vertical').setEnabled(False)

    def insert_form(self, form, button):
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget inserted in row 0: ")
        qwidget = QtWidgets.QLineEdit(form)
        form.insertWidget(0, 'inserted widget', qwidget, qlabel)
        buttonspanning = QtWidgets.QPushButton(self)
        buttonspanning.setText("Spanning widget inserted in row 2")
        form.insertWidget(2, 'inserted spanning widget', buttonspanning)
        print('\nDictionary of widgets after insertion in the form layout:\n' +
              str(form.getWidgets()))
        button.setEnabled(False)

    def onCancel(self):
        if not hasattr(self.dialog.formWidget, 'widget_states'):
            if self.dialog.getWidget('Button insert vertical').isEnabled() is False:
                self.dialog.removeWidgetFromVerticalLayout(
                    self.dialog.getWidgetFromVerticalLayout(1))

            if self.dialog.getWidget('Button insert widgets').isEnabled() is False:
                self.dialog.formWidget._popWidget(self.dialog.formWidget.default_widget_states,
                                                  'inserted widget')
                self.dialog.formWidget._popWidget(self.dialog.formWidget.default_widget_states,
                                                  'inserted spanning widget')
                self.dialog.formWidget.removeWidget('inserted widget')
                self.dialog.formWidget.removeWidget('inserted spanning widget')
        else:
            if self.dialog.getWidget('Button insert vertical').isEnabled(
            ) != self.dialog.getWidgetStates()['Button insert vertical_field']['enabled'] is True:
                self.dialog.removeWidgetFromVerticalLayout(
                    self.dialog.getWidgetFromVerticalLayout(1))
            if self.dialog.getWidget('Button insert widgets').isEnabled(
            ) != self.dialog.getWidgetStates()['Button insert widgets_field']['enabled'] is True:
                self.dialog.formWidget.removeWidget('inserted widget')
                self.dialog.formWidget.removeWidget('inserted spanning widget')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
