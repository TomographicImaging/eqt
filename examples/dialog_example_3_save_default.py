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

        self.show()

    def openFormDialog(self):
        # add a spanning widget
        self.dialog.addSpanningWidget(QtWidgets.QLabel("Input Values: "), 'input_title')
        # add all widgets
        self.dialog.addWidget(QtWidgets.QLabel('Label'), 'Label: ', 'label')
        self.dialog.addWidget(QtWidgets.QCheckBox('check me'), 'CheckBox: ', 'checkBox')
        combobox_list = ['choice 1', 'choice 2']
        self.dialog.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
        self.dialog.getWidget('comboBox').addItems(combobox_list)
        self.dialog.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
        self.dialog.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
        self.dialog.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
        self.dialog.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISlider: ', 'uiSliderWidget')
        self.dialog.addWidget(QtWidgets.QRadioButton('select me'), 'RadioButton: ', 'radioButton')
        self.dialog.addWidget(QtWidgets.QTextEdit('write text here'), 'TextEdit: ', 'textEdit')
        self.dialog.addWidget(QtWidgets.QPlainTextEdit('write text here'), 'PlainTextEdit: ',
                              'plainTextEdit')
        self.dialog.addWidget(QtWidgets.QLineEdit('write text here'), 'LineEdit: ', 'lineEdit')
        self.dialog.addWidget(QtWidgets.QPushButton('Click me'), 'Button: ', 'button')

        # redefine the onOk and onCancel functions
        self.dialog.onOk = self.accepted
        self.dialog.onCancel = self.rejected

    def accepted(self):
        print("States saved")
        self.dialog.close()

    def rejected(self):
        print("States rejected")

    # open dialog function when the parent button is clicked
    def executedialog(self):
        self.dialog.open()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
