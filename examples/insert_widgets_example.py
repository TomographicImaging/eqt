import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UIFormWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create a FormDockWidget
        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Example remove widget')
        self.addWidgetsToExampleForm(dock)

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
        buttonuser = QtWidgets.QPushButton(self)
        buttonuser.setText("inserted widget")
        print(dialog.formWidget.uiElements['verticalLayout'].count(),dialog.formWidget.uiElements['groupBoxFormLayout'].count(),dialog.formWidget.num_widgets)
        #dialog.Ok.clicked.connect(lambda: self.insert(dialog, buttonuser))
        
        
        dialog.insertWidgetVerticalLayout(3, buttonuser)
        dialog.Ok.clicked.connect(lambda: self.insert2(dialog,0, 'Widget 2',qwidget,qlabel))

        # add input as QComboBox
        dialog.addSpanningWidget(QtWidgets.QLabel("Pick the widget you want to remove:"),
                               'input_title')
        qlabel = QtWidgets.QLabel(dialog)
        qlabel.setText("User input: ")
        qwidget = QtWidgets.QComboBox(dialog)
        qwidget.addItem("Widget 2")
        qwidget.addItem("Widget 3")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        dialog.addWidget(qwidget, qlabel, 'userinput')
        print(dialog.formWidget.uiElements['verticalLayout'].count(),dialog.formWidget.uiElements['groupBoxFormLayout'].count(),dialog.formWidget.num_widgets)
        
        # add widget 1 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog)
        qlabel.setText("Widget 2: ")
        qwidget = QtWidgets.QLineEdit(dialog)
        #dialog.addWidget(qwidget,qlabel,'hello')
        dialog.insertWidget3(3, qwidget,qlabel,'hello')
        #self.addWidgetsToExampleForm(dialog)
        # dialog.addSpanningWidget(
            # QtWidgets.QLabel(
            #     "Press `Ok` to remove the user selected widget and `Cancel` to close the dialog:"),
            # 'ok_cancel_instructions')

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected

        # print dictionary of all widgets in dialog
        print("Dictionary of widgets in Form Dialog:\n" + str(self.dialog.getWidgets()))

        dialog.open()

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

    def rejected(self):
        print("\nDialog closed.")

    def insert(self, form,qwidget):
        form.insertWidgetVerticalLayout(1,qwidget)
        print("\nDictionary of widgets after insertion" + ":\n" +
              str(form.getWidgets()))
        print("insert count"+str(form.formWidget.uiElements['verticalLayout'].count()),form.formWidget.num_widgets)

    def insert2(self, form,index, name,qwidget,qlabel):
        #form.insertWidget(index, qwidget,qlabel,name)
        print("\nDictionary of widgets after insertion" + ":\n" +
              str(form.getWidgets()))
        print("insert count"+str(form.formWidget.uiElements['verticalLayout'].count()),form.formWidget.num_widgets)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
