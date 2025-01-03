from PySide2 import QtWidgets

from eqt.ui.UISliderLEditWidget import UISliderLEditWidget
from eqt.ui.UISliderWidget import UISliderWidget


def list_all_widgets():
    list_all_widgets = {
        'label': QtWidgets.QLabel('test label'), 'checkBox': QtWidgets.QCheckBox('test checkbox'),
        'comboBox': QtWidgets.QComboBox(), 'doubleSpinBox': QtWidgets.QDoubleSpinBox(),
        'spinBox': QtWidgets.QSpinBox(), 'slider': QtWidgets.QSlider(),
        'uiSliderWidget': UISliderWidget(QtWidgets.QLineEdit(), QtWidgets.QLabel()),
        'uiSliderLEditWidget': UISliderLEditWidget(),
        'radioButton': QtWidgets.QRadioButton('test radio button'),
        'textEdit': QtWidgets.QTextEdit('test text edit'),
        'plainTextEdit': QtWidgets.QPlainTextEdit('test plain text edit'),
        'lineEdit': QtWidgets.QLineEdit('test line edit'),
        'button': QtWidgets.QPushButton('test push button')}
    return list_all_widgets


def addWidgetsToExample(form):
    '''
    Adds a spanning widget and every type of widget to a form
    '''
    # add a spanning widget
    form.addSpanningWidget(QtWidgets.QLabel("Input Values: "), 'input_title')
    # add all widgets
    form.addWidget(QtWidgets.QLabel('Label'), 'Label: ', 'label')
    form.addWidget(QtWidgets.QCheckBox('check me'), 'CheckBox: ', 'checkBox')
    qwidget = QtWidgets.QComboBox()
    combobox_list = ['choice 1', 'choice 2']
    qwidget.addItems(combobox_list)
    form.addWidget(qwidget, 'ComboBox: ', 'comboBox')
    form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
    form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
    form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')

    line_edit = QtWidgets.QLineEdit()
    max_label = QtWidgets.QLabel()
    form.addWidget(
        UISliderWidget(line_edit, max_label, minimum=0.0, maximum=100.0, scale_factor=10.0),
        'UISliderWidget: ', 'uiSliderWidget')
    form.addWidget(max_label, '', 'uiSliderMaxLabel')
    form.addWidget(line_edit, '', 'uiSliderLineEdit')

    form.addWidget(UISliderLEditWidget(minimum=0.0, maximum=100.0, scale_factor=10.0),
                   'UISliderLEditWidget:', 'uiSliderLEditWidget')

    form.addWidget(QtWidgets.QRadioButton('select me'), 'RadioButton: ', 'radioButton')
    form.addWidget(QtWidgets.QTextEdit('write text here'), 'TextEdit: ', 'textEdit')
    form.addWidget(QtWidgets.QPlainTextEdit('write text here'), 'PlainTextEdit: ', 'plainTextEdit')
    form.addWidget(QtWidgets.QLineEdit('write text here'), 'LineEdit: ', 'lineEdit')
    form.addWidget(QtWidgets.QPushButton('Click me'), 'Button: ', 'button')
