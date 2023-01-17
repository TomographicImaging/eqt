import os
import sys
import unittest
from unittest import mock


try:
    print("Try to start QApplication")
    from eqt.ui.FormDialog import FormDialog
    from PySide2 import QtWidgets
    from PySide2.QtWidgets import QApplication, QPushButton
    from eqt.ui.UISliderWidget import UISliderWidget
    app = QApplication(sys.argv)
    skip_test = False
    print("We do not skip this test")
except Exception as e:
    print ("Skip this test because: ", e)
    skip_test = True


def add_every_widget_to_form(form):
    '''
    Generate every widget and add it to the form
    Parameters
    ----------
    form : FormWidget, FormDialog or FormDockWidget
        The form to add the widgets to
    '''
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


# @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
# class FormDialogStatusTest(unittest.TestCase):

#     @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
#     def setUp(self):
#         self.form = FormDialog()
#         add_every_widget_to_form(self.form)
        
#     @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
#     def test_visibility_of_widget_saved_to_state(self):
#         # Check that the visibility of the widget is saved to the state
#         # Have to use magic mock as we can't set the visibility of the QLabel
#         # to be True, because the FormDialog is not visible
#         initial_label_visibility = True
#         self.form.getWidget('label').isVisible = mock.MagicMock()
#         self.form.getWidget('label').isVisible.return_value = initial_label_visibility

#         # TODO: should we specify whether field or label?
        
#         self.assertEqual(self.form.getWidgetState('label_field')['visible'], initial_label_visibility)

#         final_label_visibility = False
#         self.form.getWidget('label').isVisible.return_value = False

#         self.assertEqual(self.form.getWidgetState('label_field')['visible'], final_label_visibility)

#     @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
#     def test_enabled_state_of_widget_saved_to_state(self):
#         # Check that the enabled state of the widget is saved to the state
        
#         initial_label_enabled_state = True

#         # TODO: should we specify whether field or label?
        
#         self.assertEqual(self.form.getWidgetState('label_field')['enabled'], initial_label_enabled_state)

#         self.form.getWidget('label').setEnabled(False)
#         final_label_enabled_state = False

#         self.assertEqual(self.form.getWidgetState('label_field')['enabled'], final_label_enabled_state)

#     @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
#     def test_value_of_QLabel_saved_to_state(self):
#         # Check that the value of the QLabel is saved to the state
        
#         initial_label_value ='test label'

#         # TODO: should we specify whether field or label?
        
#         self.assertEqual(self.form.getWidgetState('label_field')['value'], initial_label_value)

#         final_label_value = 'final test label'
#         self.form.getWidget('label').setText(final_label_value)
        
#         self.assertEqual(self.form.getWidgetState('label_field')['value'], final_label_value)
