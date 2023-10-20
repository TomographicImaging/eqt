import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog
from eqt.ui.UISliderWidget import UISliderWidget


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

        



        self.setstate(0)
        self.setstate(1)
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
        form=self.dialog
        form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
        form.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')
        form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
        form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
        form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
        form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
        form.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISliderWidget: ', 'uiSliderWidget')
        form.addWidget(QtWidgets.QRadioButton('test'), 'RadioButton: ', 'radioButton')
        form.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
        form.addWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: ', 'plainTextEdit')
        form.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')
        form.addWidget(QtWidgets.QPushButton('test'), 'Button: ', 'button')

        

        

        #redefine the onOk and onCancel functions
        self.dialog.onOk = self.accepted
        self.dialog.onCancel = self.rejected

    def setstate(self,ii):

        state=[0,0]
        state[1] = {'label_value': 'Test label state 1',
                    'checkbox_value':True,
                    'combobox_value': 1,
                    'doubleSpinBox_value': 1.0,
                    'spinBox_value': 1,
                    'slider_value': 1,
                    'uislider_value': 1,
                    'radio_value': True,
                    'textEdit_value': 'test edit 1',
                    'plainTextEdit_value': 'test plain 1',
                    'lineEdit_value': 'test line 1',
                    'button_value': True               
                    }
        
        state[0] = {'label_value': 'Test label state 0',
                    'checkbox_value':False,
                    'combobox_value': 0,
                    'doubleSpinBox_value': 10.0,
                    'spinBox_value': 10,
                    'slider_value': 10,
                    'uislider_value': 10,
                    'radio_value': False,
                    'textEdit_value': 'test edit 0',
                    'plainTextEdit_value': 'test plain 0',
                    'lineEdit_value': 'test line 0',
                    'button_value': False               
                    }

        self.dialog.getWidget('label').setText(state[ii]['label_value'])
        self.dialog.getWidget('checkBox').setChecked(state[ii]['checkbox_value'])
        
        combobox_list = ['test', 'test2']
        self.dialog.getWidget('comboBox').addItems(combobox_list)
        self.dialog.getWidget('comboBox').setCurrentIndex(state[ii]['combobox_value'])
        
        self.dialog.getWidget('doubleSpinBox').setValue(state[ii]['doubleSpinBox_value'])

        self.dialog.getWidget('spinBox').setValue(state[ii]['spinBox_value'])

        self.dialog.getWidget('slider').setValue(state[ii]['slider_value'])

        self.dialog.getWidget('uiSliderWidget').setValue(state[ii]['uislider_value'])

        self.dialog.getWidget('textEdit').setText(state[ii]['textEdit_value'])

        self.dialog.getWidget('plainTextEdit').setPlainText(state[ii]['plainTextEdit_value'])

        self.dialog.getWidget('lineEdit').setText(state[ii]['lineEdit_value'])

        self.dialog.getWidget('button').setCheckable(True)
        self.dialog.getWidget('button').setChecked(state[ii]['button_value'])

        self.dialog.getWidget('radioButton').setChecked(state[ii]['radio_value'])



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
