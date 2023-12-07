from PySide2 import QtWidgets

from eqt.ui.UISliderWidget import UISliderWidget


def addWidgetsToExample(form):
    '''
    Adds a spanning widget and every type of widget to a form
    '''
    # add a spanning widget
    form.addSpanningWidget(QtWidgets.QLabel("Input Values: "), 'input_title')
    # add all widgets
    form.addWidget(QtWidgets.QLabel('Label'), 'Label: ', 'label')
    form.addWidget(QtWidgets.QCheckBox('check me'), 'CheckBox: ', 'checkBox')
    combobox_list = ['choice 1', 'choice 2']
    form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
    form.getWidget('comboBox').addItems(combobox_list)
    form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
    form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
    form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
    form.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISlider: ', 'uiSliderWidget')
    form.addWidget(QtWidgets.QRadioButton('select me'), 'RadioButton: ', 'radioButton')
    form.addWidget(QtWidgets.QTextEdit('write text here'), 'TextEdit: ', 'textEdit')
    form.addWidget(QtWidgets.QPlainTextEdit('write text here'), 'PlainTextEdit: ', 'plainTextEdit')
    form.addWidget(QtWidgets.QLineEdit('write text here'), 'LineEdit: ', 'lineEdit')
    form.addWidget(QtWidgets.QPushButton('Click me'), 'Button: ', 'button')
