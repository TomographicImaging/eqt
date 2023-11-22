import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UIFormWidget

from eqt.ui.UISliderWidget import UISliderWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        # create a FormDockWidget
        dock = UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Example insert widget')
        #self.addWidgetsToExampleForm(dock)
        buttoninsert = QtWidgets.QPushButton(dock)
        buttoninsert.setText("Insert widgets")
        dock.addSpanningWidget(buttoninsert, 'Button insert widgets')
        buttoninsert.clicked.connect(lambda: self.insert_form(dock,buttoninsert))
        
        form = dock
        form.layout=form.widget().uiElements['groupBoxFormLayout']
        # form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
        # form.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')
        # form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
        # form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
        # form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
        # form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
        # form.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISliderWidget: ', 'uiSliderWidget')
        # form.addWidget(QtWidgets.QRadioButton('test'), 'RadioButton: ', 'radioButton')
        # form.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
        # form.addWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: ', 'plainTextEdit')
        # form.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')
        # form.addWidget(QtWidgets.QPushButton('test'), 'Button: ', 'button')
        # form.addSpanningWidget(QtWidgets.QPushButton('spanning widget'), 'spanning widget')
        
        self.test_insert_every_widget(form)

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
        #print("\nDictionary of widgets in the Form Dock Widget:\n" + str(dock.getWidgets()))


        self.show()

    def openFormDialog(self):
        dialog = FormDialog(parent=self, title='Example insert widget')
        dialog.layout=dialog.formWidget.uiElements['groupBoxFormLayout']
        #self.addWidgetsToExampleForm(dialog)
        
        form = dialog
        # form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
        # form.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')
        # form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
        # form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
        # form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
        # form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
        # form.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISliderWidget: ', 'uiSliderWidget')
        # form.addWidget(QtWidgets.QRadioButton('test'), 'RadioButton: ', 'radioButton')
        # form.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
        # form.addWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: ', 'plainTextEdit')
        # form.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')
        # form.addWidget(QtWidgets.QPushButton('test'), 'Button: ', 'button')
        # form.addSpanningWidget(QtWidgets.QPushButton('spanning widget'), 'spanning widget')

        """Generate every spanning widget and add it to `self.form`"""
        
        # form.addSpanningWidget(QtWidgets.QLabel('test label'), 'Label: s')
        # form.addSpanningWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: s')
        # form.addSpanningWidget(QtWidgets.QComboBox(), 'ComboBox: s')
        # form.addSpanningWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox:s ')
        # form.addSpanningWidget(QtWidgets.QSpinBox(), 'SpinBox:s ')
        # form.addSpanningWidget(QtWidgets.QSlider(), 'Sliders: ')
        # form.addSpanningWidget(UISliderWidget(QtWidgets.QLabel()), 'UISliderWidget:s ')
        # form.addSpanningWidget(QtWidgets.QRadioButton('test'), 'RadioButton:s ')
        # form.addSpanningWidget(QtWidgets.QTextEdit('test'), 'TextEdit:s ')
        # form.addSpanningWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: s')
        # form.addSpanningWidget(QtWidgets.QLineEdit('test'), 'LineEdit:s ')
        # form.addSpanningWidget(QtWidgets.QPushButton('test'), 'Button: s')
        
        self.test_insert_every_widget(form)


        #print(dialog.formWidget.uiElements['verticalLayout'].count(),dialog.formWidget.uiElements['groupBoxFormLayout'].count(),dialog.formWidget.num_widgets)
        dialog.Ok.clicked.connect(lambda: self.insert_vertical(dialog))
        dialog.Ok.clicked.connect(lambda: self.insert_form(dialog, dialog.Ok))
        #print(dialog.formWidget.uiElements['verticalLayout'].count(),dialog.formWidget.uiElements['groupBoxFormLayout'].count(),dialog.formWidget.num_widgets)
        
        
    
        #self.addWidgetsToExampleForm(dialog)
        # dialog.addSpanningWidget(
            # QtWidgets.QLabel(
            #     "Press `Ok` to remove the user selected widget and `Cancel` to close the dialog:"),
            # 'ok_cancel_instructions')

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected

        # print dictionary of all widgets in dialog
        #print("Dictionary of widgets in Form Dialog:\n" + str(self.dialog.getWidgets()))

        dialog.open()

    def addWidgetsToExampleForm(self, form):

        # add widget 1 as QLineEdit
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Initial widget raw 0: ")
        qwidget = QtWidgets.QLineEdit(form)
        qwidget.setClearButtonEnabled(True)
        form.addWidget(qwidget, qlabel, 'Initial widget raw 0')

        #add spanning widget
        form.addSpanningWidget(QtWidgets.QLabel("Initial widget row 1"),
                               'Initial widget row 1')
        # add input as QComboBox
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Initial widget row 2")
        qwidget = QtWidgets.QComboBox(form)
        qwidget.addItem("0")
        qwidget.addItem("1")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        form.addWidget(qwidget, qlabel, 'Initial widget row 2')

    def rejected(self):
        print("\nDialog closed.")

    def insert_vertical(self, form):
        buttonuser = QtWidgets.QPushButton(self)
        buttonuser.setText("Insert widget button bbbb")
        form.insertWidgetToVerticalLayout(1,buttonuser)
        #print("\nDictionary of widgets after insertion in the vertical lyout" + ":\n" +
              #str(form.getWidgets()))
        #print("insert count"+str(form.formWidget.uiElements['verticalLayout'].count()),form.formWidget.num_widgets)

    @property
    def list_all_widgets(self):
        list_all_widgets = [QtWidgets.QLabel('test label'), QtWidgets.QCheckBox('test checkbox'),
            QtWidgets.QComboBox(),
            QtWidgets.QDoubleSpinBox(), 
            QtWidgets.QSpinBox(), 
            QtWidgets.QSlider(), 
            UISliderWidget(QtWidgets.QLabel()), 
            QtWidgets.QRadioButton('test r adio button'), 
            QtWidgets.QTextEdit('test text edit'), 
            QtWidgets.QPlainTextEdit('test plain text edit'), 
            QtWidgets.QLineEdit('test line edit'), 
            QtWidgets.QPushButton('test push button')]
        return list_all_widgets

    def insert_form(self, form, button):
        # insert widget
        qlabel = QtWidgets.QLabel(form)
        qlabel.setText("Widget inserted in row 0: ")
        qwidget = QtWidgets.QLineEdit(form)
        form.insertWidgetToFormLayout(0, 'inserted widget', qwidget, qlabel)
        
        buttonuser = QtWidgets.QPushButton(self)
        buttonuser.setText("Inserted widget in row 2")
        form.insertWidgetToFormLayout(2, 'inserted spanning widget', buttonuser)
        
        #print("\nDictionary of widgets after insertion in the form layout" + ":\n" +
        #      str(form.getWidgets()))
        button.setEnabled(False)

    def _test_insert_one_widget(self, form, row,name, qwidget, qlabel=None):
        form.insertWidgetToFormLayout(row,f'{name}',qwidget,qlabel)
        #position=self.layout.getWidgetPosition(self.form.getWidget(name,'field'))[0]
        #self.assertEqual(position, row)
        #form.insertWidgetToFormLayout(row,f'{name}_spanning',qwidget)
        #position=self.layout.getWidgetPosition(self.form.getWidget(name,'field'))[0]
        #self.assertEqual(position, row)
        
        
        


    def test_insert_every_widget(self,form):
        """Insert every widget from `self.form`"""
        list_widgets_names = [
            'label insert', 'checkBox insert', 'comboBox insert', 'doubleSpinBox insert', 'spinBox insert', 'slider insert',
            'uiSliderWidget insert', 'radioButton insert', 'textEdit insert', 'plainTextEdit insert', 'lineEdit insert', 'button insert']
        for i in range(0,len(self.list_all_widgets)):
            #print(self.list_all_widgets[i])
            qwidget = self.list_all_widgets[i]
            #qlabel = QtWidgets.QLabel(form)
            name = list_widgets_names[i]
            self._test_insert_one_widget(form,0,name,qwidget,name)
            qwidget = self.list_all_widgets[i]
            self._test_insert_one_widget(form,0,name+' spanning',qwidget)
            print(name+' spanning')



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
