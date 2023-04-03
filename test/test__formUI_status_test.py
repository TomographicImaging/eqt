import os
import sys
import unittest
from unittest import mock

from eqt.ui.FormDialog import FormDialog
from eqt.ui.UIFormWidget import FormWidget, FormDockWidget
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication
from eqt.ui.UISliderWidget import UISliderWidget


# skip the tests on GitHub actions
if os.environ.get('CONDA_BUILD', '0') == '1':
    skip_test = True
else:
    skip_test = False

print("skip_test is set to ", skip_test)


if not skip_test:
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
else:
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
    form.addWidget(QtWidgets.QCheckBox(
        'test checkbox'), 'CheckBox: ', 'checkBox')
    form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
    form.addWidget(QtWidgets.QDoubleSpinBox(),
                   'DoubleSpinBox: ', 'doubleSpinBox')
    form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
    form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
    form.addWidget(UISliderWidget(QtWidgets.QLabel()),
                   'UISliderWidget: ', 'uiSliderWidget')
    form.addWidget(QtWidgets.QRadioButton('test'),
                   'RadioButton: ', 'radioButton')
    form.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
    form.addWidget(QtWidgets.QPlainTextEdit('test'),
                   'PlainTextEdit: ', 'plainTextEdit')
    form.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')
    form.addWidget(QtWidgets.QPushButton('test'), 'Button: ', 'button')


def add_two_widgets_to_form(form):
    '''
    Generate two widgets and add them to the form

    Parameters
    ----------
    form : FormWidget, FormDialog or FormDockWidget
        The form to add the widgets to
    '''
    form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
    form.addWidget(QtWidgets.QCheckBox(
        'test checkbox'), 'CheckBox: ', 'checkBox')


@unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
class FormDialogStatusTest(unittest.TestCase):

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def setUp(self):
        self.form = FormDialog()
        add_every_widget_to_form(self.form)
        self.simple_form = FormDialog()
        add_two_widgets_to_form(self.simple_form)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_visibility(self):
        # Check that the visibility of the widget is saved to the state
        # Have to use magic mock as we can't set the visibility of the QLabel
        # to be True, because the FormDialog is not visible
        initial_label_visibility = True
        self.form.getWidget('label').isVisible = mock.MagicMock()
        self.form.getWidget(
            'label').isVisible.return_value = initial_label_visibility

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'visible'], initial_label_visibility)

        final_label_visibility = False
        self.form.getWidget('label').isVisible.return_value = False

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'visible'], final_label_visibility)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_enabled_state(self):
        # Check that the enabled state of the widget is saved to the state

        initial_label_enabled_state = True

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'enabled'], initial_label_enabled_state)

        self.form.getWidget('label').setEnabled(False)
        final_label_enabled_state = False

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'enabled'], final_label_enabled_state)

    # Test value is saved for all widget types ----------------------------------------------------------------

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QLabel_value(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'Label: '

        self.assertEqual(self.form.getWidgetState(
            'label_label')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label', 'label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label_label')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_role_parameter_field(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_role_parameter_label(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_default_role_parameter(self):
        # Check that the value of the QLabel is saved to the state
        initial_label_value = 'test label'

        # In getWidgetState we do not specify if we want the 'field' or 'label' role, so it should default to 'field':
        self.assertEqual(self.form.getWidgetState(
            'label')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QCheckBox_value(self):
        # Check that the value of the QCheckBox is saved to the state

        initial_checkbox_value = False

        self.assertEqual(self.form.getWidgetState('checkBox_field')[
                         'value'], initial_checkbox_value)

        final_checkbox_value = True
        self.form.getWidget('checkBox').setChecked(final_checkbox_value)

        self.assertEqual(self.form.getWidgetState(
            'checkBox_field')['value'], final_checkbox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QComboBox_value(self):
        # Check that the value of the QComboBox is saved to the state

        combobox_list = ['test', 'test2']
        self.form.getWidget('comboBox').addItems(combobox_list)

        initial_combobox_value = 0

        self.assertEqual(self.form.getWidgetState('comboBox_field')[
                         'value'], initial_combobox_value)

        final_combobox_value = 1
        self.form.getWidget('comboBox').setCurrentIndex(final_combobox_value)

        self.assertEqual(self.form.getWidgetState(
            'comboBox_field')['value'], final_combobox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QDoubleSpinBox_value(self):
        # Check that the value of the QDoubleSpinBox is saved to the state

        initial_doubleSpinBox_value = 0.0

        self.assertEqual(self.form.getWidgetState('doubleSpinBox_field')[
                         'value'], initial_doubleSpinBox_value)

        final_doubleSpinBox_value = 1.0
        self.form.getWidget('doubleSpinBox').setValue(
            final_doubleSpinBox_value)

        self.assertEqual(self.form.getWidgetState('doubleSpinBox_field')[
                         'value'], final_doubleSpinBox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QSpinBox_value(self):
        # Check that the value of the QSpinBox is saved to the state

        initial_spinBox_value = 0

        self.assertEqual(self.form.getWidgetState('spinBox_field')[
                         'value'], initial_spinBox_value)

        final_spinBox_value = 1
        self.form.getWidget('spinBox').setValue(final_spinBox_value)

        self.assertEqual(self.form.getWidgetState(
            'spinBox_field')['value'], final_spinBox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QSlider_value(self):
        # Check that the value of the QSlider is saved to the state

        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState(
            'slider_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('slider').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState(
            'slider_field')['value'], final_slider_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_UISliderWidget_value(self):
        # Check that the value of the UISliderWidget is returned in the state

        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState(
            'uiSliderWidget_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('uiSliderWidget').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState(
            'uiSliderWidget_field')['value'], final_slider_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QLineEdit_value(self):
        # Check that the value of the QLineEdit is saved to the state

        initial_lineEdit_value = ''
        self.form.getWidget('lineEdit').setText(initial_lineEdit_value)

        self.assertEqual(self.form.getWidgetState('lineEdit_field')[
                         'value'], initial_lineEdit_value)

        final_lineEdit_value = 'test'
        self.form.getWidget('lineEdit').setText(final_lineEdit_value)

        self.assertEqual(self.form.getWidgetState(
            'lineEdit_field')['value'], final_lineEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QTextEdit_value(self):
        # Check that the value of the QTextEdit is saved to the state

        initial_textEdit_value = ''
        self.form.getWidget('textEdit').setText(initial_textEdit_value)

        self.assertEqual(self.form.getWidgetState('textEdit_field')[
                         'value'], initial_textEdit_value)

        final_textEdit_value = 'test'
        self.form.getWidget('textEdit').setText(final_textEdit_value)

        self.assertEqual(self.form.getWidgetState(
            'textEdit_field')['value'], final_textEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QPlainTextEdit_value(self):
        # Check that the value of the QPlainTextEdit is saved to the state

        initial_plainTextEdit_value = ''
        self.form.getWidget('plainTextEdit').setPlainText(
            initial_plainTextEdit_value)

        self.assertEqual(self.form.getWidgetState('plainTextEdit_field')[
                         'value'], initial_plainTextEdit_value)

        final_plainTextEdit_value = 'test'
        self.form.getWidget('plainTextEdit').setPlainText(
            final_plainTextEdit_value)

        self.assertEqual(self.form.getWidgetState('plainTextEdit_field')[
                         'value'], final_plainTextEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QPushButton_value(self):
        # Check that the value of the QPushButton is saved to the state

        initial_button_value = False

        self.assertEqual(self.form.getWidgetState(
            'button_field')['value'], initial_button_value)

        final_button_value = True
        self.form.getWidget('button').setCheckable(True)
        self.form.getWidget('button').setChecked(final_button_value)

        self.assertEqual(self.form.getWidgetState(
            'button_field')['value'], final_button_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QRadioButton_value(self):
        # Check that the value of the QRadioButton is saved to the state

        initial_radio_value = False

        self.assertEqual(self.form.getWidgetState(
            'radioButton_field')['value'], initial_radio_value)

        final_radio_value = True
        self.form.getWidget('radioButton').setChecked(final_radio_value)

        self.assertEqual(self.form.getWidgetState(
            'radioButton_field')['value'], final_radio_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetStates(self):
        state_to_set = {
            'checkBox_field': {'value': True, 'enabled': False, 'visible': False},
            'label_field': {'value': 'applyWidgetStates Test', 'enabled': True, 'visible': False}
        }

        self.simple_form.applyWidgetStates(state_to_set)

        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox_field'), state_to_set['checkBox_field'])
        self.assertEqual(self.simple_form.getWidgetState(
            'label_field'), state_to_set['label_field'])

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState('checkBox_field', state_to_set)
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox_field'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_field(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState(
            'checkBox', state_to_set, role='field')
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox', 'field'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_label(self):
        state_to_set = {'value': 'test the checkbox:',
                        'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState(
            'checkBox', state_to_set, role='label')
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox', 'label'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_default(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState('checkBox', state_to_set)
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getAllWidgetStates(self):
        # Check that the state of all widgets is returned

        expected_state = {
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False},
            'label_field': {'value': 'test label', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label: ', 'enabled': True, 'visible': False}
        }

        self.assertEqual(self.simple_form.getAllWidgetStates(), expected_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_saveAllWidgetStates(self):
        # Check that the state of all widgets is saved to the state variable

        expected_state = {
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False},
            'label_field': {'value': 'test label', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label: ', 'enabled': True, 'visible': False}
        }

        self.simple_form.saveAllWidgetStates()

        self.assertEqual(
            self.simple_form.formWidget.widget_states, expected_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_restoreAllSavedWidgetStates(self):
        # Check that the state of all widgets is restored from the state variable

        state_to_restore = {
            'checkBox_field': {'value': True, 'enabled': False, 'visible': False},
            'label_field': {'value': 'applyWidgetStates Test', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox Test: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label Test: ', 'enabled': True, 'visible': False}
        }

        self.simple_form.formWidget.widget_states = state_to_restore

        self.simple_form.restoreAllSavedWidgetStates()

        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isChecked(), state_to_restore['checkBox_field']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isEnabled(), state_to_restore['checkBox_field']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isVisible(), state_to_restore['checkBox_field']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').text(), state_to_restore['checkBox_label']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').isEnabled(), state_to_restore['checkBox_label']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').isVisible(), state_to_restore['checkBox_label']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'label').text(), state_to_restore['label_field']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'label').isEnabled(), state_to_restore['label_field']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'label').isVisible(), state_to_restore['label_field']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').text(), state_to_restore['label_label']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').isEnabled(), state_to_restore['label_label']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').isVisible(), state_to_restore['label_label']['visible'])


@unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
class FormWidgetStateTest(unittest.TestCase):

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def setUp(self):
        self.form = FormWidget()
        add_every_widget_to_form(self.form)
        self.simple_form = FormWidget()
        add_two_widgets_to_form(self.simple_form)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_visibility(self):
        # Check that the visibility of the widget is saved to the state
        # Have to use magic mock as we can't set the visibility of the QLabel
        # to be True, because the FormDialog is not visible
        initial_label_visibility = True
        self.form.getWidget('label').isVisible = mock.MagicMock()
        self.form.getWidget(
            'label').isVisible.return_value = initial_label_visibility

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'visible'], initial_label_visibility)

        final_label_visibility = False
        self.form.getWidget('label').isVisible.return_value = False

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'visible'], final_label_visibility)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_enabled_state(self):
        # Check that the enabled state of the widget is saved to the state

        initial_label_enabled_state = True

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'enabled'], initial_label_enabled_state)

        self.form.getWidget('label').setEnabled(False)
        final_label_enabled_state = False

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'enabled'], final_label_enabled_state)

    # Test value is saved for all widget types ----------------------------------------------------------------

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_role_parameter_field(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_role_parameter_label(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_default_role_parameter(self):
        # Check that the value of the QLabel is saved to the state
        initial_label_value = 'test label'

        # In getWidgetState we do not specify if we want the 'field' or 'label' role, so it should default to 'field':
        self.assertEqual(self.form.getWidgetState(
            'label')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QLabel_value(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label_field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label_field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QCheckBox_value(self):
        # Check that the value of the QCheckBox is saved to the state

        initial_checkbox_value = False

        self.assertEqual(self.form.getWidgetState('checkBox_field')[
                         'value'], initial_checkbox_value)

        final_checkbox_value = True
        self.form.getWidget('checkBox').setChecked(final_checkbox_value)

        self.assertEqual(self.form.getWidgetState(
            'checkBox_field')['value'], final_checkbox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QComboBox_value(self):
        # Check that the value of the QComboBox is saved to the state

        combobox_list = ['test', 'test2']
        self.form.getWidget('comboBox').addItems(combobox_list)

        initial_combobox_value = 0

        self.assertEqual(self.form.getWidgetState('comboBox_field')[
                         'value'], initial_combobox_value)

        final_combobox_value = 1
        self.form.getWidget('comboBox').setCurrentIndex(final_combobox_value)

        self.assertEqual(self.form.getWidgetState(
            'comboBox_field')['value'], final_combobox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QDoubleSpinBox_value(self):
        # Check that the value of the QDoubleSpinBox is saved to the state

        initial_doubleSpinBox_value = 0.0

        self.assertEqual(self.form.getWidgetState('doubleSpinBox_field')[
                         'value'], initial_doubleSpinBox_value)

        final_doubleSpinBox_value = 1.0
        self.form.getWidget('doubleSpinBox').setValue(
            final_doubleSpinBox_value)

        self.assertEqual(self.form.getWidgetState('doubleSpinBox_field')[
                         'value'], final_doubleSpinBox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QSpinBox_value(self):
        # Check that the value of the QSpinBox is saved to the state

        initial_spinBox_value = 0

        self.assertEqual(self.form.getWidgetState('spinBox_field')[
                         'value'], initial_spinBox_value)

        final_spinBox_value = 1
        self.form.getWidget('spinBox').setValue(final_spinBox_value)

        self.assertEqual(self.form.getWidgetState(
            'spinBox_field')['value'], final_spinBox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QSlider_value(self):
        # Check that the value of the QSlider is saved to the state

        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState(
            'slider_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('slider').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState(
            'slider_field')['value'], final_slider_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_UISliderWidget_value(self):
        # Check that the value of the UISliderWidget is returned in the state

        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState(
            'uiSliderWidget_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('uiSliderWidget').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState(
            'uiSliderWidget_field')['value'], final_slider_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QLineEdit_value(self):
        # Check that the value of the QLineEdit is saved to the state

        initial_lineEdit_value = ''
        self.form.getWidget('lineEdit').setText(initial_lineEdit_value)

        self.assertEqual(self.form.getWidgetState('lineEdit_field')[
                         'value'], initial_lineEdit_value)

        final_lineEdit_value = 'test'
        self.form.getWidget('lineEdit').setText(final_lineEdit_value)

        self.assertEqual(self.form.getWidgetState(
            'lineEdit_field')['value'], final_lineEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QTextEdit_value(self):
        # Check that the value of the QTextEdit is saved to the state

        initial_textEdit_value = ''
        self.form.getWidget('textEdit').setText(initial_textEdit_value)

        self.assertEqual(self.form.getWidgetState('textEdit_field')[
                         'value'], initial_textEdit_value)

        final_textEdit_value = 'test'
        self.form.getWidget('textEdit').setText(final_textEdit_value)

        self.assertEqual(self.form.getWidgetState(
            'textEdit_field')['value'], final_textEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QPlainTextEdit_value(self):
        # Check that the value of the QPlainTextEdit is saved to the state

        initial_plainTextEdit_value = ''
        self.form.getWidget('plainTextEdit').setPlainText(
            initial_plainTextEdit_value)

        self.assertEqual(self.form.getWidgetState('plainTextEdit_field')[
                         'value'], initial_plainTextEdit_value)

        final_plainTextEdit_value = 'test'
        self.form.getWidget('plainTextEdit').setPlainText(
            final_plainTextEdit_value)

        self.assertEqual(self.form.getWidgetState('plainTextEdit_field')[
                         'value'], final_plainTextEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QPushButton_value(self):
        # Check that the value of the QPushButton is saved to the state

        initial_button_value = False

        self.assertEqual(self.form.getWidgetState(
            'button_field')['value'], initial_button_value)

        final_button_value = True
        self.form.getWidget('button').setCheckable(True)
        self.form.getWidget('button').setChecked(final_button_value)

        self.assertEqual(self.form.getWidgetState(
            'button_field')['value'], final_button_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QRadioButton_value(self):
        # Check that the value of the QRadioButton is saved to the state

        initial_radio_value = False

        self.assertEqual(self.form.getWidgetState(
            'radioButton_field')['value'], initial_radio_value)

        final_radio_value = True
        self.form.getWidget('radioButton').setChecked(final_radio_value)

        self.assertEqual(self.form.getWidgetState(
            'radioButton_field')['value'], final_radio_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetStates(self):
        state_to_set = {
            'checkBox_field': {'value': True, 'enabled': False, 'visible': False},
            'label_field': {'value': 'applyWidgetStates Test', 'enabled': True, 'visible': False}
        }

        self.simple_form.applyWidgetStates(state_to_set)

        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox_field'), state_to_set['checkBox_field'])
        self.assertEqual(self.simple_form.getWidgetState(
            'label_field'), state_to_set['label_field'])

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState('checkBox_field', state_to_set)
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox_field'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_field(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState(
            'checkBox', state_to_set, role='field')
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox', 'field'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_label(self):
        state_to_set = {'value': 'test the checkbox:',
                        'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState(
            'checkBox', state_to_set, role='label')
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox', 'label'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_default(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState('checkBox', state_to_set)
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getAllWidgetStates(self):
        # Check that the state of all widgets is returned

        expected_state = {
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False},
            'label_field': {'value': 'test label', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label: ', 'enabled': True, 'visible': False}
        }

        self.assertEqual(self.simple_form.getAllWidgetStates(), expected_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_saveAllWidgetStates(self):
        # Check that the state of all widgets is saved to the state variable

        expected_state = {
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False},
            'label_field': {'value': 'test label', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label: ', 'enabled': True, 'visible': False}
        }

        self.simple_form.saveAllWidgetStates()

        self.assertEqual(self.simple_form.widget_states, expected_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_restoreAllSavedWidgetStates(self):
        # Check that the state of all widgets is restored from the state variable

        state_to_restore = {
            'checkBox_field': {'value': True, 'enabled': False, 'visible': False},
            'label_field': {'value': 'applyWidgetStates Test', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox Test: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label Test: ', 'enabled': True, 'visible': False}
        }

        self.simple_form.widget_states = state_to_restore

        self.simple_form.restoreAllSavedWidgetStates()

        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isChecked(), state_to_restore['checkBox_field']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isEnabled(), state_to_restore['checkBox_field']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isVisible(), state_to_restore['checkBox_field']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').text(), state_to_restore['checkBox_label']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').isEnabled(), state_to_restore['checkBox_label']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').isVisible(), state_to_restore['checkBox_label']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'label').text(), state_to_restore['label_field']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'label').isEnabled(), state_to_restore['label_field']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'label').isVisible(), state_to_restore['label_field']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').text(), state_to_restore['label_label']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').isEnabled(), state_to_restore['label_label']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').isVisible(), state_to_restore['label_label']['visible'])


@unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
class FormDockWidgetStateTest(unittest.TestCase):

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def setUp(self):
        self.form = FormDockWidget()
        add_every_widget_to_form(self.form)
        self.simple_form = FormDockWidget()
        add_two_widgets_to_form(self.simple_form)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_visibility(self):
        # Check that the visibility of the widget is saved to the state
        # Have to use magic mock as we can't set the visibility of the QLabel
        # to be True, because the FormDialog is not visible
        initial_label_visibility = True
        self.form.getWidget('label').isVisible = mock.MagicMock()
        self.form.getWidget(
            'label').isVisible.return_value = initial_label_visibility

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'visible'], initial_label_visibility)

        final_label_visibility = False
        self.form.getWidget('label').isVisible.return_value = False

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'visible'], final_label_visibility)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_enabled_state(self):
        # Check that the enabled state of the widget is saved to the state

        initial_label_enabled_state = True

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'enabled'], initial_label_enabled_state)

        self.form.getWidget('label').setEnabled(False)
        final_label_enabled_state = False

        self.assertEqual(self.form.getWidgetState('label_field')[
                         'enabled'], final_label_enabled_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_role_parameter_field(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_role_parameter_label(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label', 'field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_value_using_default_role_parameter(self):
        # Check that the value of the QLabel is saved to the state
        initial_label_value = 'test label'

        # In getWidgetState we do not specify if we want the 'field' or 'label' role, so it should default to 'field':
        self.assertEqual(self.form.getWidgetState(
            'label')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label')['value'], final_label_value)

    # Test value is saved for all widget types ----------------------------------------------------------------

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QLabel_value(self):
        # Check that the value of the QLabel is saved to the state

        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState(
            'label_field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState(
            'label_field')['value'], final_label_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QCheckBox_value(self):
        # Check that the value of the QCheckBox is saved to the state

        initial_checkbox_value = False

        self.assertEqual(self.form.getWidgetState('checkBox_field')[
                         'value'], initial_checkbox_value)

        final_checkbox_value = True
        self.form.getWidget('checkBox').setChecked(final_checkbox_value)

        self.assertEqual(self.form.getWidgetState(
            'checkBox_field')['value'], final_checkbox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QComboBox_value(self):
        # Check that the value of the QComboBox is saved to the state

        combobox_list = ['test', 'test2']
        self.form.getWidget('comboBox').addItems(combobox_list)

        initial_combobox_value = 0

        self.assertEqual(self.form.getWidgetState('comboBox_field')[
                         'value'], initial_combobox_value)

        final_combobox_value = 1
        self.form.getWidget('comboBox').setCurrentIndex(final_combobox_value)

        self.assertEqual(self.form.getWidgetState(
            'comboBox_field')['value'], final_combobox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QDoubleSpinBox_value(self):
        # Check that the value of the QDoubleSpinBox is saved to the state

        initial_doubleSpinBox_value = 0.0

        self.assertEqual(self.form.getWidgetState('doubleSpinBox_field')[
                         'value'], initial_doubleSpinBox_value)

        final_doubleSpinBox_value = 1.0
        self.form.getWidget('doubleSpinBox').setValue(
            final_doubleSpinBox_value)

        self.assertEqual(self.form.getWidgetState('doubleSpinBox_field')[
                         'value'], final_doubleSpinBox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QSpinBox_value(self):
        # Check that the value of the QSpinBox is saved to the state

        initial_spinBox_value = 0

        self.assertEqual(self.form.getWidgetState('spinBox_field')[
                         'value'], initial_spinBox_value)

        final_spinBox_value = 1
        self.form.getWidget('spinBox').setValue(final_spinBox_value)

        self.assertEqual(self.form.getWidgetState(
            'spinBox_field')['value'], final_spinBox_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QSlider_value(self):
        # Check that the value of the QSlider is saved to the state

        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState(
            'slider_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('slider').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState(
            'slider_field')['value'], final_slider_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_UISliderWidget_value(self):
        # Check that the value of the UISliderWidget is returned in the state

        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState(
            'uiSliderWidget_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('uiSliderWidget').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState(
            'uiSliderWidget_field')['value'], final_slider_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QLineEdit_value(self):
        # Check that the value of the QLineEdit is saved to the state

        initial_lineEdit_value = ''
        self.form.getWidget('lineEdit').setText(initial_lineEdit_value)

        self.assertEqual(self.form.getWidgetState('lineEdit_field')[
                         'value'], initial_lineEdit_value)

        final_lineEdit_value = 'test'
        self.form.getWidget('lineEdit').setText(final_lineEdit_value)

        self.assertEqual(self.form.getWidgetState(
            'lineEdit_field')['value'], final_lineEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QTextEdit_value(self):
        # Check that the value of the QTextEdit is saved to the state

        initial_textEdit_value = ''
        self.form.getWidget('textEdit').setText(initial_textEdit_value)

        self.assertEqual(self.form.getWidgetState('textEdit_field')[
                         'value'], initial_textEdit_value)

        final_textEdit_value = 'test'
        self.form.getWidget('textEdit').setText(final_textEdit_value)

        self.assertEqual(self.form.getWidgetState(
            'textEdit_field')['value'], final_textEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QPlainTextEdit_value(self):
        # Check that the value of the QPlainTextEdit is saved to the state

        initial_plainTextEdit_value = ''
        self.form.getWidget('plainTextEdit').setPlainText(
            initial_plainTextEdit_value)

        self.assertEqual(self.form.getWidgetState('plainTextEdit_field')[
                         'value'], initial_plainTextEdit_value)

        final_plainTextEdit_value = 'test'
        self.form.getWidget('plainTextEdit').setPlainText(
            final_plainTextEdit_value)

        self.assertEqual(self.form.getWidgetState('plainTextEdit_field')[
                         'value'], final_plainTextEdit_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QPushButton_value(self):
        # Check that the value of the QPushButton is saved to the state

        initial_button_value = False

        self.assertEqual(self.form.getWidgetState(
            'button_field')['value'], initial_button_value)

        final_button_value = True
        self.form.getWidget('button').setCheckable(True)
        self.form.getWidget('button').setChecked(final_button_value)

        self.assertEqual(self.form.getWidgetState(
            'button_field')['value'], final_button_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getWidgetState_returns_QRadioButton_value(self):
        # Check that the value of the QRadioButton is saved to the state

        initial_radio_value = False

        self.assertEqual(self.form.getWidgetState(
            'radioButton_field')['value'], initial_radio_value)

        final_radio_value = True
        self.form.getWidget('radioButton').setChecked(final_radio_value)

        self.assertEqual(self.form.getWidgetState(
            'radioButton_field')['value'], final_radio_value)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetStates(self):
        state_to_set = {
            'checkBox_field': {'value': True, 'enabled': False, 'visible': False},
            'label_field': {'value': 'applyWidgetStates Test', 'enabled': True, 'visible': False}
        }

        self.simple_form.applyWidgetStates(state_to_set)

        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox_field'), state_to_set['checkBox_field'])
        self.assertEqual(self.simple_form.getWidgetState(
            'label_field'), state_to_set['label_field'])

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState('checkBox_field', state_to_set)
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox_field'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_field(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState(
            'checkBox', state_to_set, role='field')
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox', 'field'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_label(self):
        state_to_set = {'value': 'test the checkbox:',
                        'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState(
            'checkBox', state_to_set, role='label')
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox', 'label'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_applyWidgetState_using_role_parameter_default(self):
        state_to_set = {'value': True, 'enabled': False, 'visible': False}
        self.simple_form.applyWidgetState('checkBox', state_to_set)
        self.assertEqual(self.simple_form.getWidgetState(
            'checkBox'), state_to_set)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_getAllWidgetStates(self):
        # Check that the state of all widgets is returned

        expected_state = {
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False},
            'label_field': {'value': 'test label', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label: ', 'enabled': True, 'visible': False}
        }

        self.assertEqual(self.simple_form.getAllWidgetStates(), expected_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_saveAllWidgetStates(self):
        # Check that the state of all widgets is saved to the state variable

        expected_state = {
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False},
            'label_field': {'value': 'test label', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label: ', 'enabled': True, 'visible': False}
        }

        self.simple_form.saveAllWidgetStates()

        self.assertEqual(
            self.simple_form.widget().widget_states, expected_state)

    @unittest.skipIf(skip_test, "Can't test interfaces if we can't connect to the display")
    def test_restoreAllSavedWidgetStates(self):
        # Check that the state of all widgets is restored from the state variable

        state_to_restore = {
            'checkBox_field': {'value': True, 'enabled': False, 'visible': False},
            'label_field': {'value': 'applyWidgetStates Test', 'enabled': True, 'visible': False},
            'checkBox_label': {'value': 'CheckBox Test: ', 'enabled': True, 'visible': False},
            'label_label': {'value': 'Label Test: ', 'enabled': True, 'visible': False}
        }

        self.simple_form.widget().widget_states = state_to_restore

        self.simple_form.restoreAllSavedWidgetStates()

        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isChecked(), state_to_restore['checkBox_field']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isEnabled(), state_to_restore['checkBox_field']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox').isVisible(), state_to_restore['checkBox_field']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').text(), state_to_restore['checkBox_label']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').isEnabled(), state_to_restore['checkBox_label']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'checkBox', 'label').isVisible(), state_to_restore['checkBox_label']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'label').text(), state_to_restore['label_field']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'label').isEnabled(), state_to_restore['label_field']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'label').isVisible(), state_to_restore['label_field']['visible'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').text(), state_to_restore['label_label']['value'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').isEnabled(), state_to_restore['label_label']['enabled'])
        self.assertEqual(self.simple_form.getWidget(
            'label', 'label').isVisible(), state_to_restore['label_label']['visible'])


if __name__ == '__main__':
    unittest.main()
