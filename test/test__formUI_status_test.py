import abc
import unittest
from unittest import mock

from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtTest import QTest

from eqt.ui.FormDialog import AdvancedFormDialog, FormDialog
from eqt.ui.UIFormWidget import FormDockWidget, FormWidget
from eqt.ui.UISliderWidget import UISliderWidget

from . import is_ci, skip

if is_ci:
    skip("Running in CI (no GUI)", allow_module_level=True)


class FormsCommonTests(metaclass=abc.ABCMeta):
    """Common tests for all Form types"""
    @abc.abstractmethod
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.
        """
        self.form = None # stop mypy [attr-defined] error
        raise NotImplementedError

    @property
    def exampleState(self):
        # define two states for every widget
        state = [{
            'label_value': 'Test label state 0', 'checkBox_value': False, 'comboBox_value': 0,
            'doubleSpinBox_value': 10.0, 'spinBox_value': 10, 'slider_value': 10,
            'uiSliderWidget_value': 10, 'radioButton_value': False,
            'textEdit_value': 'test edit 0', 'plainTextEdit_value': 'test plain 0',
            'lineEdit_value': 'test line 0', 'button_value': False}, {
                'label_value': 'Test label state 1', 'checkBox_value': True, 'comboBox_value': 1,
                'doubleSpinBox_value': 1.0, 'spinBox_value': 1, 'slider_value': 1,
                'uiSliderWidget_value': 1, 'radioButton_value': True,
                'textEdit_value': 'test edit 1', 'plainTextEdit_value': 'test plain 1',
                'lineEdit_value': 'test line 1', 'button_value': True}]
        return state

    @property
    def list_all_widgets(self):
        combobox_widget = QtWidgets.QComboBox()
        combobox_list = ['choice 1', 'choice 2']
        combobox_widget.addItems(combobox_list)
        list_all_widgets = {
            'label': QtWidgets.QLabel('test label'),
            'checkBox': QtWidgets.QCheckBox('test checkbox'), 'comboBox': combobox_widget,
            'doubleSpinBox': QtWidgets.QDoubleSpinBox(), 'spinBox': QtWidgets.QSpinBox(),
            'slider': QtWidgets.QSlider(), 'uiSliderWidget': UISliderWidget(QtWidgets.QLabel()),
            'radioButton': QtWidgets.QRadioButton('test radio button'),
            'textEdit': QtWidgets.QTextEdit('test text edit'),
            'plainTextEdit': QtWidgets.QPlainTextEdit('test plain text edit'),
            'lineEdit': QtWidgets.QLineEdit('test line edit'),
            'button': QtWidgets.QPushButton('test push button')}
        return list_all_widgets

    @property
    def state_simple_form(self):
        state_simple_form = {
            'label_field': {
                'value': 'test label', 'enabled': True, 'visible': False,
                'widget_row': 0}, 'label_label': {
                    'value': 'Label: ', 'enabled': True, 'visible': False, 'widget_row': 0},
            'checkBox_field': {'value': False, 'enabled': True, 'visible': False, 'widget_row': 1},
            'checkBox_label': {
                'value': 'CheckBox: ', 'enabled': True, 'visible': False, 'widget_row': 1}}
        return state_simple_form

    def add_every_widget(self):
        """Generate every widget and add it to the form."""
        form = self.form
        for key in self.list_all_widgets:
            form.addWidget(self.list_all_widgets[key], key, key)

    def add_two_widgets(self):
        """Generate two widgets and add them to `self.simple_form`"""
        form = self.simple_form
        form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
        form.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')

    def set_state(self, i: int):
        """
        Applies the values saved in `self.exampleState` at position `i` to the widgets in the form.
        """
        state = self.exampleState
        # set the states
        # QLabel
        self.form.getWidget('label').setText(state[i]['label_value'])
        # QCheckBox
        self.form.getWidget('checkBox').setChecked(state[i]['checkBox_value'])
        # QComboBox
        combobox_list = ['test', 'test2']
        self.form.getWidget('comboBox').addItems(combobox_list)
        self.form.getWidget('comboBox').setCurrentIndex(state[i]['comboBox_value'])
        # QDoubleSpinBox
        self.form.getWidget('doubleSpinBox').setValue(state[i]['doubleSpinBox_value'])
        # QSpinBox
        self.form.getWidget('spinBox').setValue(state[i]['spinBox_value'])
        # QSlider
        self.form.getWidget('slider').setValue(state[i]['slider_value'])
        # UISlider
        self.form.getWidget('uiSliderWidget').setValue(state[i]['uiSliderWidget_value'])
        # QRadioButton
        self.form.getWidget('radioButton').setChecked(state[i]['radioButton_value'])
        # QTextEdit
        self.form.getWidget('textEdit').setText(state[i]['textEdit_value'])
        # QPlainTextEdit
        self.form.getWidget('plainTextEdit').setPlainText(state[i]['plainTextEdit_value'])
        # QLineEdit
        self.form.getWidget('lineEdit').setText(state[i]['lineEdit_value'])
        # QPushButton
        self.form.getWidget('button').setCheckable(True)
        self.form.getWidget('button').setChecked(state[i]['button_value'])

    def set_spanning_state(self, i: int):
        """
        Applies the values saved in `self.exampleState` at position `i`
        to the spanning widgets in the form.
        """
        state = self.exampleState
        # set the states
        # QLabel
        self.form.getWidget('label_spanning').setText(state[i]['label_value'])
        # QCheckBox
        self.form.getWidget('checkBox_spanning').setChecked(state[i]['checkBox_value'])
        # QComboBox
        combobox_list = ['test', 'test2']
        self.form.getWidget('comboBox_spanning').addItems(combobox_list)
        self.form.getWidget('comboBox_spanning').setCurrentIndex(state[i]['comboBox_value'])
        # QDoubleSpinBox
        self.form.getWidget('doubleSpinBox_spanning').setValue(state[i]['doubleSpinBox_value'])
        # QSpinBox
        self.form.getWidget('spinBox_spanning').setValue(state[i]['spinBox_value'])
        # QSlider
        self.form.getWidget('slider_spanning').setValue(state[i]['slider_value'])
        # UISlider
        self.form.getWidget('uiSliderWidget_spanning').setValue(state[i]['uiSliderWidget_value'])
        # QRadioButton
        self.form.getWidget('radioButton_spanning').setChecked(state[i]['radioButton_value'])
        # QTextEdit
        self.form.getWidget('textEdit_spanning').setText(state[i]['textEdit_value'])
        # QPlainTextEdit
        self.form.getWidget('plainTextEdit_spanning').setPlainText(state[i]['plainTextEdit_value'])
        # QLineEdit
        self.form.getWidget('lineEdit_spanning').setText(state[i]['lineEdit_value'])
        # QPushButton
        self.form.getWidget('button_spanning').setCheckable(True)
        self.form.getWidget('button_spanning').setChecked(state[i]['button_value'])

    def _test_add_one_widget(self, name, qwidget, qlabel):
        """
        Invokes `addWidget`, therefore inserts the qwidget and the qlabel
        at the end of the layout. Checks the position of the widget in the form is the last one.
        """
        self.form.addWidget(qwidget, qlabel, name)
        position = self.layout.getWidgetPosition(self.form.getWidget(name, 'field'))[0]
        self.assertEqual(position, self.form.getNumWidgets() - 1)

    def _test_add_one_spanning_widget(self, name, qwidget):
        """
        Invokes `addSpanningWidget`, therefore inserts the qwidget
        at the end of the layout. Checks the position of the widget in the form is the last one.
        """
        name = f'{name}_spanning'
        self.form.addSpanningWidget(qwidget, name)
        position = self.layout.getWidgetPosition(self.form.getWidget(name, 'field'))[0]
        self.assertEqual(position, self.form.getNumWidgets() - 1)

    def test_add_every_widget(self):
        """
        Adds each widget, and then each spanning widget, in the end of the form layout.
        Tests the position of the widgets in the layout is the last one.
        """
        for key in self.list_all_widgets:
            qwidget = self.list_all_widgets[key]
            name = f'{key}_added'
            self._test_add_one_widget(name, qwidget, name)
            qwidget = self.list_all_widgets[key]
            self._test_add_one_spanning_widget(name + '_spanning', qwidget)

    def _test_insert_one_widget(self, row, name, qwidget, qlabel=None):
        """
        Invokes `insertWidget`, therefore inserts the qwidget (and the qlabel)
        at position row in the layout. Checks the position of the widget in the form is `row`.
        """
        self.form.insertWidget(row, f'{name}', qwidget, qlabel)
        position = self.layout.getWidgetPosition(self.form.getWidget(name, 'field'))[0]
        self.assertEqual(position, row)

    def test_insert_every_widget(self):
        """
        Inserts each widget, and then each spanning widget, in position 0 of the form layout.
        Tests the position of the widgets in the layout is 0.
        """
        for key, qwidget in self.list_all_widgets.items():
            name = f'{key}_insert'
            self._test_insert_one_widget(0, name, qwidget, name)
            qwidget = self.list_all_widgets[key]
            self._test_insert_one_widget(0, name + '_spanning', qwidget)

    def _test_remove_one_widget(self, name):
        """
        Removes one widget.
        Checks the number of widgets in the form before and after deletion are consistent.
        Checks the number of rows in the layout and number of widgets in the form are
        consistent.
        ----------------
        name: name in the dictionary of the widget to be removed
        """
        qwidget = self.form.getWidget(name, role='field')
        rowpre, role = self.layout.getWidgetPosition(qwidget) # checks the widget exists
        prerowcount = self.layout.rowCount()
        predictionary = self.form.getWidgets().copy()
        prenumwidgets = self.form.getNumWidgets()
        self.form.removeWidget(name)
        postrowcount = self.layout.rowCount()
        postdictionary = self.form.getWidgets()
        postnumwidgets = self.form.getNumWidgets()
        self.assertNotEqual(predictionary, postdictionary)
        self.assertEqual(prenumwidgets, postnumwidgets + 1)
        self.assertEqual(prerowcount, postrowcount + 1)
        self.assertEqual(postrowcount, postnumwidgets)

    def test_remove_every_widget(self):
        """Remove every widget from the form."""
        for name in self.list_all_widgets:
            self._test_remove_one_widget(name)

    def test_getWidgetState_returns_visibility(self):
        """
        Check that the visibility of the widget is saved to the state
        Have to use magic mock as we can't set the visibility of the QLabel
        to be True, because the FormDialog is not visible
        """
        initial_label_visibility = True
        self.form.getWidget('label').isVisible = mock.MagicMock()
        self.form.getWidget('label').isVisible.return_value = initial_label_visibility

        self.assertEqual(
            self.form.getWidgetState('label_field')['visible'], initial_label_visibility)

        final_label_visibility = False
        self.form.getWidget('label').isVisible.return_value = False

        self.assertEqual(
            self.form.getWidgetState('label_field')['visible'], final_label_visibility)

    def test_getWidgetState_returns_enabled_state(self):
        """Check that the enabled state of the widget is saved to the state"""

        initial_label_enabled_state = True

        self.assertEqual(
            self.form.getWidgetState('label_field')['enabled'], initial_label_enabled_state)

        self.form.getWidget('label').setEnabled(False)
        final_label_enabled_state = False

        self.assertEqual(
            self.form.getWidgetState('label_field')['enabled'], final_label_enabled_state)

    def test_getWidgetState_returns_value_using_role_parameter_field(self):
        """Check that the value of the QLabel is saved to the state"""
        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState('label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState('label', 'field')['value'], final_label_value)

    def test_getWidgetState_returns_value_using_role_parameter_label(self):
        """Check that the value of the QLabel is saved to the state"""
        initial_label_value = 'test label'

        self.assertEqual(self.form.getWidgetState('label', 'field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState('label', 'field')['value'], final_label_value)

    def test_getWidgetState_returns_value_using_default_role_parameter(self):
        """Check that the value of the QLabel is saved to the state"""
        initial_label_value = 'test label'

        # `getWidgetState` doesn't specify 'field' or 'label' role, so default to 'field'
        self.assertEqual(self.form.getWidgetState('label')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)

        self.assertEqual(self.form.getWidgetState('label')['value'], final_label_value)

    def test_getWidgetState_returns_QCheckBox_value(self):
        """Check that the value of the QCheckBox is saved to the state"""
        initial_checkbox_value = False

        self.assertEqual(
            self.form.getWidgetState('checkBox_field')['value'], initial_checkbox_value)

        final_checkbox_value = True
        self.form.getWidget('checkBox').setChecked(final_checkbox_value)

        self.assertEqual(self.form.getWidgetState('checkBox_field')['value'], final_checkbox_value)

    def test_getWidgetState_returns_QComboBox_value(self):
        """Check that the value of the QComboBox is saved to the state"""
        combobox_list = ['test', 'test2']
        self.form.getWidget('comboBox').addItems(combobox_list)

        initial_combobox_value = 0

        self.assertEqual(
            self.form.getWidgetState('comboBox_field')['value'], initial_combobox_value)

        final_combobox_value = 1
        self.form.getWidget('comboBox').setCurrentIndex(final_combobox_value)

        self.assertEqual(self.form.getWidgetState('comboBox_field')['value'], final_combobox_value)

    def test_getWidgetState_returns_QDoubleSpinBox_value(self):
        """Check that the value of the QDoubleSpinBox is saved to the state"""
        initial_doubleSpinBox_value = 0.0

        self.assertEqual(
            self.form.getWidgetState('doubleSpinBox_field')['value'], initial_doubleSpinBox_value)

        final_doubleSpinBox_value = 1.0
        self.form.getWidget('doubleSpinBox').setValue(final_doubleSpinBox_value)

        self.assertEqual(
            self.form.getWidgetState('doubleSpinBox_field')['value'], final_doubleSpinBox_value)

    def test_getWidgetState_returns_QSpinBox_value(self):
        """Check that the value of the QSpinBox is saved to the state"""
        initial_spinBox_value = 0

        self.assertEqual(self.form.getWidgetState('spinBox_field')['value'], initial_spinBox_value)

        final_spinBox_value = 1
        self.form.getWidget('spinBox').setValue(final_spinBox_value)

        self.assertEqual(self.form.getWidgetState('spinBox_field')['value'], final_spinBox_value)

    def test_getWidgetState_returns_QSlider_value(self):
        """Check that the value of the QSlider is saved to the state"""
        initial_slider_value = 0

        self.assertEqual(self.form.getWidgetState('slider_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('slider').setValue(final_slider_value)

        self.assertEqual(self.form.getWidgetState('slider_field')['value'], final_slider_value)

    def test_getWidgetState_returns_UISliderWidget_value(self):
        """Check that the value of the UISliderWidget is returned in the state"""
        initial_slider_value = 0

        self.assertEqual(
            self.form.getWidgetState('uiSliderWidget_field')['value'], initial_slider_value)

        final_slider_value = 1
        self.form.getWidget('uiSliderWidget').setValue(final_slider_value)

        self.assertEqual(
            self.form.getWidgetState('uiSliderWidget_field')['value'], final_slider_value)

    def test_getWidgetState_returns_QLineEdit_value(self):
        """Check that the value of the QLineEdit is saved to the state"""
        initial_lineEdit_value = ''
        self.form.getWidget('lineEdit').setText(initial_lineEdit_value)

        self.assertEqual(
            self.form.getWidgetState('lineEdit_field')['value'], initial_lineEdit_value)

        final_lineEdit_value = 'test'
        self.form.getWidget('lineEdit').setText(final_lineEdit_value)

        self.assertEqual(self.form.getWidgetState('lineEdit_field')['value'], final_lineEdit_value)

    def test_getWidgetState_returns_QTextEdit_value(self):
        """Check that the value of the QTextEdit is saved to the state"""
        initial_textEdit_value = ''
        self.form.getWidget('textEdit').setText(initial_textEdit_value)

        self.assertEqual(
            self.form.getWidgetState('textEdit_field')['value'], initial_textEdit_value)

        final_textEdit_value = 'test'
        self.form.getWidget('textEdit').setText(final_textEdit_value)

        self.assertEqual(self.form.getWidgetState('textEdit_field')['value'], final_textEdit_value)

    def test_getWidgetState_returns_QPlainTextEdit_value(self):
        """Check that the value of the QPlainTextEdit is saved to the state"""
        initial_plainTextEdit_value = ''
        self.form.getWidget('plainTextEdit').setPlainText(initial_plainTextEdit_value)

        self.assertEqual(
            self.form.getWidgetState('plainTextEdit_field')['value'], initial_plainTextEdit_value)

        final_plainTextEdit_value = 'test'
        self.form.getWidget('plainTextEdit').setPlainText(final_plainTextEdit_value)

        self.assertEqual(
            self.form.getWidgetState('plainTextEdit_field')['value'], final_plainTextEdit_value)

    def test_getWidgetState_returns_QPushButton_value(self):
        """Check that the value of the QPushButton is saved to the state"""
        initial_button_value = False

        self.assertEqual(self.form.getWidgetState('button_field')['value'], initial_button_value)

        final_button_value = True
        self.form.getWidget('button').setCheckable(True)
        self.form.getWidget('button').setChecked(final_button_value)

        self.assertEqual(self.form.getWidgetState('button_field')['value'], final_button_value)

    def test_getWidgetState_returns_QRadioButton_value(self):
        """Check that the value of the QRadioButton is saved to the state"""
        initial_radio_value = False

        self.assertEqual(
            self.form.getWidgetState('radioButton_field')['value'], initial_radio_value)

        final_radio_value = True
        self.form.getWidget('radioButton').setChecked(final_radio_value)

        self.assertEqual(self.form.getWidgetState('radioButton_field')['value'], final_radio_value)

    def test_applyWidgetStates(self):
        self.simple_form.applyWidgetStates(self.state_simple_form)

        self.assertEqual(self.simple_form.getWidgetState('checkBox_field'),
                         self.state_simple_form['checkBox_field'])
        self.assertEqual(self.simple_form.getWidgetState('label_field'),
                         self.state_simple_form['label_field'])

    def test_applyWidgetState(self):
        self.simple_form.applyWidgetState('checkBox', self.state_simple_form['checkBox_field'])
        self.assertEqual(self.simple_form.getWidgetState('checkBox'),
                         self.state_simple_form['checkBox_field'])

    def test_applyWidgetState_using_role_parameter_field(self):
        self.simple_form.applyWidgetState('checkBox', self.state_simple_form['checkBox_field'],
                                          role='field')
        self.assertEqual(self.simple_form.getWidgetState('checkBox', 'field'),
                         self.state_simple_form['checkBox_field'])

    def test_applyWidgetState_using_role_parameter_label(self):
        self.simple_form.applyWidgetState('checkBox', self.state_simple_form['checkBox_label'],
                                          role='label')
        self.assertEqual(self.simple_form.getWidgetState('checkBox', 'label'),
                         self.state_simple_form['checkBox_label'])

    def test_applyWidgetState_using_role_parameter_default(self):
        self.simple_form.applyWidgetState('checkBox', self.state_simple_form['checkBox_field'])
        self.assertEqual(self.simple_form.getWidgetState('checkBox'),
                         self.state_simple_form['checkBox_field'])

    def test_getAllWidgetStates(self):
        """Check that the state of all widgets is returned"""
        self.assertEqual(self.simple_form.getAllWidgetStates(), self.state_simple_form)


class FormWidgetStateTest(FormsCommonTests, unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.
        """
        self.form = FormWidget()
        self.add_every_widget()
        self.simple_form = FormWidget()
        self.add_two_widgets()
        self.layout = self.form.uiElements['groupBoxFormLayout']

    def test_get_name_and_role_from_key_or_widget(self):
        """
        Checks that the method `_getNameAndRoleFromKey` returns the correct name and role in
        all widgets.
        """
        for name in self.list_all_widgets:
            for role in {'field', 'label'}:
                name_role = name + '_' + role
                name_c, role_c = self.form._getNameAndRoleFromKey(name_role)
                self.assertEqual(name_c, name)
                self.assertEqual(role_c, role)
                name_c, role_c = self.form._getNameAndRoleFromWidget(
                    self.form.getWidget(name, role))
                self.assertEqual(name_c, name)
                self.assertEqual(role_c, role)

    def test_getWidgetState_returns_QLabel_value(self):
        """Check that the value of the QLabel is saved to the state"""
        initial_label_value = 'test label'
        self.assertEqual(self.form.getWidgetState('label_field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)
        self.assertEqual(self.form.getWidgetState('label_field')['value'], final_label_value)

    def test_saveAllWidgetStates(self):
        """Check that the state of all widgets is saved to the state variable"""
        self.simple_form.saveAllWidgetStates()
        self.assertEqual(self.simple_form.widget_states, self.state_simple_form)

    def test_restoreAllSavedWidgetStates(self):
        """Check that the state of all widgets is restored from the state variable"""
        state_to_restore = self.state_simple_form
        self.simple_form.widget_states = self.state_simple_form
        self.simple_form.restoreAllSavedWidgetStates()

        self.assertEqual(
            self.simple_form.getWidget('checkBox').isChecked(),
            state_to_restore['checkBox_field']['value'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox').isEnabled(),
            state_to_restore['checkBox_field']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox').isVisible(),
            state_to_restore['checkBox_field']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').text(),
            state_to_restore['checkBox_label']['value'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').isEnabled(),
            state_to_restore['checkBox_label']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').isVisible(),
            state_to_restore['checkBox_label']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('label').text(), state_to_restore['label_field']['value'])
        self.assertEqual(
            self.simple_form.getWidget('label').isEnabled(),
            state_to_restore['label_field']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('label').isVisible(),
            state_to_restore['label_field']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').text(),
            state_to_restore['label_label']['value'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').isEnabled(),
            state_to_restore['label_label']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').isVisible(),
            state_to_restore['label_label']['visible'])


class FormDockWidgetStateTest(FormsCommonTests, unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.
        """
        self.form = FormDockWidget()
        self.add_every_widget()
        self.simple_form = FormDockWidget()
        self.add_two_widgets()
        self.layout = self.form.widget().uiElements['groupBoxFormLayout']

    def test_form_init_title(self):
        """Tests if the FormDockWidget is created correctly with or without the title argument."""
        FormDockWidget()
        FormDockWidget(title=None)
        FormDockWidget(title='title')

    def test_getWidgetState_returns_QLabel_value(self):
        """Check that the value of the QLabel is saved to the state"""
        initial_label_value = 'test label'
        self.assertEqual(self.form.getWidgetState('label_field')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)
        self.assertEqual(self.form.getWidgetState('label_field')['value'], final_label_value)

    def test_saveAllWidgetStates(self):
        """Check that the state of all widgets is saved to the state variable"""
        self.simple_form.saveAllWidgetStates()
        self.assertEqual(self.simple_form.widget().widget_states, self.state_simple_form)

    def test_restoreAllSavedWidgetStates(self):
        """Check that the state of all widgets is restored from the state variable"""
        state_to_restore = self.state_simple_form
        self.simple_form.widget().widget_states = self.state_simple_form
        self.simple_form.restoreAllSavedWidgetStates()

        self.assertEqual(
            self.simple_form.getWidget('checkBox').isChecked(),
            state_to_restore['checkBox_field']['value'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox').isEnabled(),
            state_to_restore['checkBox_field']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox').isVisible(),
            state_to_restore['checkBox_field']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').text(),
            state_to_restore['checkBox_label']['value'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').isEnabled(),
            state_to_restore['checkBox_label']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').isVisible(),
            state_to_restore['checkBox_label']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('label').text(), state_to_restore['label_field']['value'])
        self.assertEqual(
            self.simple_form.getWidget('label').isEnabled(),
            state_to_restore['label_field']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('label').isVisible(),
            state_to_restore['label_field']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').text(),
            state_to_restore['label_label']['value'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').isEnabled(),
            state_to_restore['label_label']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').isVisible(),
            state_to_restore['label_label']['visible'])


class FormDialogStatusTest(FormsCommonTests, unittest.TestCase):
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.
        """
        self.form = FormDialog()
        self.add_every_widget()
        self.simple_form = FormDialog()
        self.add_two_widgets()
        self.layout = self.form.formWidget.uiElements['groupBoxFormLayout']
        self.vertical_layout = self.form.formWidget.uiElements['verticalLayout']

    def click_Ok(self):
        """
        Clicks the ok button on the form.

        This method simulates a mouse click on the ok button in the form.
        """
        QTest.mouseClick(self.form.Ok, Qt.LeftButton)

    def click_Cancel(self):
        """
        Clicks the cancel button on the form.

        This method simulates a mouse click on the cancel button in the form.
        """
        QTest.mouseClick(self.form.Cancel, Qt.LeftButton)

    def add_every_widget_to_vertical_layout(self):
        """Add every widget to the vertical layout."""
        for key in self.list_all_widgets:
            self.form.addWidget(self.list_all_widgets[key], qlabel=None, name=None,
                                layout='vertical')

    def test_Ok_and_Cancel_button_behaviour(self):
        # create the states dictionary
        self.set_state(1)
        states1 = self.form.getAllWidgetStates()
        self.set_state(0)
        states0 = self.form.getAllWidgetStates()
        # check state 0 and 1 are not saved when Cancel is pressed
        self.click_Cancel()
        self.assertNotEqual(states0, self.form.getAllWidgetStates())
        self.assertNotEqual(states1, self.form.getAllWidgetStates())
        # save state 0
        self.set_state(0)
        self.assertEqual(states0, self.form.getAllWidgetStates())
        self.click_Ok()
        self.assertEqual(states0, self.form.getAllWidgetStates())
        # save state 1
        self.set_state(1)
        self.assertEqual(states1, self.form.getAllWidgetStates())
        self.click_Ok()
        self.assertEqual(states1, self.form.getAllWidgetStates())
        # change to state 0 without saving
        self.set_state(0)
        self.assertEqual(states0, self.form.getAllWidgetStates())
        self.click_Cancel()
        self.assertEqual(states1, self.form.getAllWidgetStates())

    def test_form_init_title(self):
        """Tests if the FormDialog is created correctly with or without the title argument."""
        FormDialog()
        FormDialog(title=None)
        FormDialog(title='title')

    def _test_insert_one_widget_to_vertical_layout(self, row, qwidget):
        """
        Invokes `insertWidgetToVerticalLayout`, therefore inserts the qwidget at position
        row in the layout. Checks the position of the widget in the form is `row`.
        """
        self.form.insertWidgetToVerticalLayout(row, qwidget)
        position = self.vertical_layout.indexOf(qwidget)
        self.assertEqual(position, row)

    def _test_add_one_widget_to_vertical_layout(self, qwidget):
        """
        Invokes `addWidget` with vertical layout. Therefore adds the qwidget
        at the end of the layout. Checks that the widget inserted is the inputted one and
        its position in the layout corresponds to the number of widgets in the layout
        before insertion.
        """
        num_widgets = self.vertical_layout.count()
        self.form.addWidget(qwidget, layout='vertical')
        index = self.form.getIndexFromVerticalLayout(qwidget)
        self.assertEqual(index, num_widgets)
        widget = self.vertical_layout.itemAt(num_widgets).widget()
        self.assertEqual(qwidget, widget)

    def _test_add_one_spanning_widget_to_vertical_layout(self, qwidget):
        """
        Invokes `addSpanningWidget` with vertical layout. Therefore adds the qwidget
        at the end of the layout. Checks that the widget inserted is the inputted one and
        its position in the layout corresponds to the number of widgets in the layout
        before insertion.
        """
        num_widgets = self.vertical_layout.count()
        self.form.addSpanningWidget(qwidget, layout='vertical')
        index = self.form.getIndexFromVerticalLayout(qwidget)
        self.assertEqual(index, num_widgets)
        widget = self.vertical_layout.itemAt(num_widgets).widget()
        self.assertEqual(qwidget, widget)

    def test_insert_every_widget_to_vertical_layout(self):
        """
        Inserts each widget in position 0 of the vertical layout and tests its position in
        the layout is 0.
        """
        for key in self.list_all_widgets:
            self._test_insert_one_widget_to_vertical_layout(0, self.list_all_widgets[key])

    def test_add_every_widget_to_vertical_layout(self):
        """
        Adds each widget and each spanning widget at the end of the vertical layout and tests them.
        """
        for key in self.list_all_widgets:
            self._test_add_one_widget_to_vertical_layout(self.list_all_widgets[key])
            self._test_add_one_spanning_widget_to_vertical_layout(self.list_all_widgets[key])

    def _test_remove_one_widget_from_vertical_layout(self, widget):
        """
        Removes one widget from the vertical layout.
        Checks the number of items in the layout before and after deletion are consistent.

        Parameters
        ----------
        widget: qwidget to be removed
        """
        qwidget = self.form.getWidgetFromVerticalLayout(2)
        prerowcount = self.vertical_layout.count()
        self.form.removeWidgetFromVerticalLayout(qwidget)
        postrowcount = self.vertical_layout.count()
        self.assertEqual(prerowcount, postrowcount + 1)

    def test_remove_every_widget_from_vertical_layout(self):
        """Remove every widget from the vertical layout."""
        self.add_every_widget_to_vertical_layout()
        for widget in self.list_all_widgets.items():
            self._test_remove_one_widget_from_vertical_layout(widget)

    def test_getWidgetState_returns_QLabel_value(self):
        """Check that the value of the QLabel is saved to the state"""
        initial_label_value = 'label'
        self.assertEqual(self.form.getWidgetState('label_label')['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label', 'label').setText(final_label_value)
        self.assertEqual(self.form.getWidgetState('label_label')['value'], final_label_value)

    def test_saveAllWidgetStates(self):
        """Check that the state of all widgets is saved to the state variable"""
        self.simple_form.saveAllWidgetStates()
        self.assertEqual(self.simple_form.formWidget.widget_states, self.state_simple_form)

    def test_restoreAllSavedWidgetStates(self):
        """Check that the state of all widgets is restored from the state variable"""
        state_to_restore = self.state_simple_form
        self.simple_form.formWidget.widget_states = self.state_simple_form
        self.simple_form.restoreAllSavedWidgetStates()

        self.assertEqual(
            self.simple_form.getWidget('checkBox').isChecked(),
            state_to_restore['checkBox_field']['value'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox').isEnabled(),
            state_to_restore['checkBox_field']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox').isVisible(),
            state_to_restore['checkBox_field']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').text(),
            state_to_restore['checkBox_label']['value'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').isEnabled(),
            state_to_restore['checkBox_label']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('checkBox', 'label').isVisible(),
            state_to_restore['checkBox_label']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('label').text(), state_to_restore['label_field']['value'])
        self.assertEqual(
            self.simple_form.getWidget('label').isEnabled(),
            state_to_restore['label_field']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('label').isVisible(),
            state_to_restore['label_field']['visible'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').text(),
            state_to_restore['label_label']['value'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').isEnabled(),
            state_to_restore['label_label']['enabled'])
        self.assertEqual(
            self.simple_form.getWidget('label', 'label').isVisible(),
            state_to_restore['label_label']['visible'])


class AdvancedFormDialogStatusTest(FormDialogStatusTest):
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.

        An advanced form dialog with no parent is created.
        """
        self.form = AdvancedFormDialog(title='Advanced form dialog without parent')
        self.layout = self.form.formWidget.uiElements['groupBoxFormLayout']
        self.vertical_layout = self.form.formWidget.uiElements['verticalLayout']
        self.add_every_widget()
        self.simple_form = AdvancedFormDialog()
        self.add_two_widgets()

    def click_default_button(self):
        """
        Clicks the default button on the form.

        This method simulates a mouse click on the default button of the form.
        """
        QTest.mouseClick(self.form.default_button, Qt.LeftButton)

    def test_position_default_button(self):
        """Checks the default button is created in the advanced dialog with and without parent.
        Asserts the button's position is 1, hence is located between the form layout and
        the ok and cancel buttons."""
        index = self.form.getIndexFromVerticalLayout(self.form.default_button)
        self.assertEqual(index, 1)

    def test_default_button_behaviour(self):
        """
        Tests the behavior of the default button on the advanced dialog.

        This test case opens the dialog, updates the widgets, clicks the default
        button and then the Ok button. Verifies that the widgets in the dialog
        are set to their default states.
        """
        self.form.open()
        self.set_state(0)
        self.click_default_button()
        self.click_Ok()
        self.assertEqual(self.form.getSavedWidgetStates(), self.form.getDefaultWidgetStates())


class AdvancedFormDialogWithParentStatusTest(AdvancedFormDialogStatusTest):
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.

        An advanced form dialog with parent is created.
        """
        self.form_parent = FormWidget()
        self.form_parent.addSpanningWidget(QtWidgets.QPushButton("Open Advanced Dialog"),
                                           'button_advanced')
        self.form = AdvancedFormDialog(parent=self.form_parent, title='Advanced form dialog',
                                       parent_button_name='button_advanced')

        self.layout = self.form.formWidget.uiElements['groupBoxFormLayout']
        self.vertical_layout = self.form.formWidget.uiElements['verticalLayout']
        self.add_every_widget()
        for key in self.list_all_widgets:
            self.form.displayWidgetValueOnParent(key)

        self.simple_form = AdvancedFormDialog()
        self.add_two_widgets()

    def _test_parent_state(self, i):
        """
        Gets the parent widget states and compares them with the expected states.
        If the value in the parent originated from the ComboBox in the advanced dialog,
        it is converted to its corresponding index in the comboBox before comparison.
        """
        parent_states = self.form_parent.getAllWidgetStates()
        for name in self.list_all_widgets:
            if isinstance(self.list_all_widgets[name], QtWidgets.QComboBox):
                value = parent_states[f'{name}_field']['value']
                parent_states[f'{name}_field']['value'] = str(
                    self.form.getWidget(name, 'field').findText(value))
            self.assertEqual(parent_states[f'{name}_field']['value'],
                             str(self.exampleState[i][f'{name}_value']))
            self.assertEqual(parent_states[f'{name}_label']['value'], name)

    def test_ok_button_behaviour(self):
        """
        Tests the behavior of the Ok button on the advanced dialog.

        This test case verifies the button's behavior in different scenarios:
        1. Clicks the Ok button without changing any states and verifies that the parent
        widget states remain unchanged.
        2. Changes the states and click the OK button, then verifies that the parent widget
        states are updated correctly.
        3. Clicks the default button and then the OK button, and verifies that the parent widget
        states are restored to their initial values.
        """
        # 1.
        parent_initial_states = self.form_parent.getAllWidgetStates()
        self.form.open()
        self.click_Ok()
        parent_states = self.form_parent.getAllWidgetStates()
        self.assertEqual(parent_states, parent_initial_states)
        # 2.
        for i in [0, 1]:
            self.set_state(i)
            self.form.open()
            self.click_Ok()
            self._test_parent_state(i)
        # 3.
        self.form.open()
        self.click_default_button()
        self.click_Ok()
        parent_states = self.form_parent.getAllWidgetStates()
        self.assertEqual(parent_states, parent_initial_states)

    def test_cancel_button_behaviour(self):
        """
        Tests the behavior of the Cancel button on the advanced dialog.

        This test case verifies the button's behavior in different scenarios:
        1. Opens the dialog, clicks the Cancel button without changing any states and verifies that
        the parent-widget states remain unchanged.
        2. Opens the dialog, update the widgets and clicks the Cancel button. Verifies that the
        parent-widget states remain unchanged.
        3. Opens the dialog, updates the widgets and clicks the Ok button. Then reopens the dialog,
        changes the states and clicks the Cancel button. Verifies that the parent widget states are
        those set before reopening the dialog.
        4. Opens the dialog, clicks the default button and then the Cancel button. Verifies that
        the parent widget states remain unchanged.
        """
        # 1.
        parent_initial_states = self.form_parent.getAllWidgetStates()
        self.form.open()
        self.click_Cancel()
        parent_states = self.form_parent.getAllWidgetStates()
        self.assertEqual(parent_states, parent_initial_states)
        # 2.
        self.form.open()
        self.set_state(0)
        self.click_Cancel()
        parent_states = self.form_parent.getAllWidgetStates()
        self.assertEqual(parent_states, parent_initial_states)
        # 3.
        self.form.open()
        self.set_state(0)
        self.click_Ok()
        self.form.open()
        self.set_state(1)
        self.click_Cancel()
        self._test_parent_state(0)
        # 4.
        self.form.open()
        self.click_default_button()
        self.click_Cancel()
        self._test_parent_state(0)
        """
        Tests the behavior of the default button on the advanced dialog.

        This test case opens the dialog, updates the widgets, clicks the default
        button and then the Ok button. Verifies that the widgets in the dialog
        are set to their default states.
        """
        self.form.open()
        self.set_state(0)
        self.click_default_button()
        self.click_Ok()
        self.assertEqual(self.form.getSavedWidgetStates(), self.form.getDefaultWidgetStates())

    def test_button_argument(self):
        "Checks that the widgets are placed in the expected rows under the parent button."
        self.set_state(0)
        self.click_Ok()
        for index, name in enumerate(self.list_all_widgets, start=1):
            row = self.form_parent.getWidgetRow(name)
            self.assertEqual(row, self.form.parent_button_row + index)


class AdvancedFormDialogNoButtonArgumentStatusTest(AdvancedFormDialogWithParentStatusTest):
    def setUp(self):
        """
        Set up the test environment by initialising the necessary objects and widgets.
        This method is executed before each test case.

        An advanced form dialog with parent and no argument `parent_button_name` is created.
        """
        self.form_parent = FormWidget()
        self.form_parent.addSpanningWidget(QtWidgets.QPushButton("Open Advanced Dialog"),
                                           'button_advanced')
        self.form = AdvancedFormDialog(parent=self.form_parent, title='Advanced form dialog')

        self.layout = self.form.formWidget.uiElements['groupBoxFormLayout']
        self.vertical_layout = self.form.formWidget.uiElements['verticalLayout']
        self.add_every_widget()
        for name in self.list_all_widgets:
            self.form.displayWidgetValueOnParent(name)

        self.simple_form = AdvancedFormDialog()
        self.add_two_widgets()

    def test_button_argument(self):
        "Checks that the widgets are placed in the expected row in the parent layout."
        num_initial = self.form_parent.getNumWidgets()
        self.set_state(0)
        self.click_Ok()
        for index, name in enumerate(self.list_all_widgets):
            row = self.form_parent.getWidgetRow(name)
            self.assertEqual(row, num_initial + index)
