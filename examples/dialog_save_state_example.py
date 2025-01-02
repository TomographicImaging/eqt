import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog
from eqt.ui.UISliderLEditWidget import UISliderLEditWidget
from eqt.ui.UISliderWidget import UISliderWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with form layout")
        pb.clicked.connect(lambda: self.openFormDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        # create dialog to be opened later:
        dialog = FormDialog(parent=self, title='Example')

        # ## Example on how to add elements to the
        dialog.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
        dialog.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')

        combobox = QtWidgets.QComboBox()
        combobox.addItems(['test1', 'test2'])
        dialog.addWidget(combobox, 'ComboBox: ', 'comboBox')

        dialog.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
        dialog.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
        dialog.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')

        line_edit = QtWidgets.QLineEdit()
        max_label = QtWidgets.QLabel()
        dialog.addWidget(
            UISliderWidget(line_edit, max_label, minimum=0.0, maximum=100.0, scale_factor=10.0),
            'UISliderWidget: ', 'uiSliderWidget')
        dialog.addWidget(max_label, '', 'input_max_label1')
        dialog.addWidget(line_edit, '', 'input_line_edit1')

        dialog.addWidget(UISliderLEditWidget(minimum=0.0, maximum=100.0, scale_factor=10.0),
                         'UISliderLEditWidget:', 'uiSliderLEditWidget')

        dialog.addWidget(QtWidgets.QRadioButton('test 1'), 'RadioButton 1: ', 'radioButton1')
        dialog.addWidget(QtWidgets.QRadioButton('test 2'), 'RadioButton 2: ', 'radioButton2')
        dialog.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
        dialog.addWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: ', 'plainTextEdit')
        dialog.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')

        button = QtWidgets.QPushButton('test')
        button.setCheckable(True)
        dialog.addWidget(button, 'Button: ', 'button')

        # store a reference
        self.dialog = dialog

        self.show()

    def openFormDialog(self):
        self.dialog.exec()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
