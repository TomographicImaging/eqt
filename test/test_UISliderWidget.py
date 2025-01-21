import unittest

from parameterized import parameterized
from qtpy import QtGui
from qtpy.QtWidgets import QGridLayout, QLabel, QLineEdit, QSlider

from eqt.ui import UISliderWidget

from . import skip_ci


@skip_ci
class TestUISliderWidget(unittest.TestCase):
    def setUp(self):
        self.test_widgets = {
            "standard": {"minimum": 0.0,
                         "maximum": 10.0}, "positive": {"minimum": 1.0, "maximum": 10.0},
            "negative": {"minimum": -10.0,
                         "maximum": -1.0}, "float": {"minimum": -0.5, "maximum": 0.5},
            "long": {"minimum": 1.11111, "maximum": 9.99999}}

    @parameterized.expand([("standard", 0.0, 10.0), ("positive", 1.0, 10.0),
                           ("negative", -10.0, -1.0), ("float", -0.5, 0.5), ("long", 1.11, 10.0)])
    def test_init_widget(self, _, expected_minimum, expected_maximum):
        '''Tests widget instantiation using different 'minimum'/'maximum' arguments.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
        self.assertIsInstance(widget, UISliderWidget.UISliderWidget)
        self.assertEqual(widget.minimum, expected_minimum)
        self.assertEqual(widget.maximum, expected_maximum)

    def test_init_default_properties(self):
        '''Tests the setting of the widget's default properties.
        '''
        for widget in self.test_widgets.values():
            minimum = widget.get("minimum")
            maximum = widget.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
            self.assertEqual(widget.decimals, 2)
            self.assertEqual(widget.number_of_steps, 2000)
            self.assertEqual(widget.number_of_ticks, 10)

    @parameterized.expand([("standard", 5.0), ("positive", 5.5), ("negative", -5.5),
                           ("float", 0.0), ("long", 5.5600000000000005)])
    def test_init_median(self, _, median):
        '''Tests the calculation of the 'median' property.
        '''
        for widget in self.test_widgets.values():
            widget = self.test_widgets.get(_)
            self.assertEqual(widget.median, median)

    def test_widget_state(self):
        '''Tests the widget default widget states.
        '''
        for widget in self.test_widgets.values():
            self.assertTrue(widget.isVisible())
            self.assertTrue(widget.isEnabled())

    @parameterized.expand([("min_gt_max", 10.0, 0.0), ("min_eq_max", 0.0, 0.0)])
    def test_input_invalid_min_max(self, _, minimum, maximum):
        '''Tests for correct widget behaviour when invalid combinations
        of 'minimum'/'maximum' are supplied.
        '''
        with self.assertRaises(ValueError):
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

    @parameterized.expand([("positive", 10, 10), ("negative", -10, 0), ("float", 2.5, 2),
                           ("long", 9.99999, 9)])
    def test_input_decimals(self, _, decimals, expected):
        '''Tests the correct widget behaviour when different 'decimals'
        arguments are supplied.
        If an invalid argument is supplied, a ValueError is raised.
        '''

        try:
            self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                        decimals=decimals)
            self.assertEqual(self.widget.decimals, expected)
        except ValueError:
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                            decimals=decimals)

    @parameterized.expand([("positive", 1500, 1500, 0.0006666666666666666),
                           ("negative", -50, 2000, 0.0005), ("float", 2.5, 2, 0.5),
                           ("long", 9.99999, 9, 0.11111111111111111111111111111111)])
    def test_input_number_of_steps(self, name, number_of_steps, expected_steps, expected_size):
        '''Tests the correct widget behaviour when different 'number_of_steps'
        arguments are supplied.
        If an invalid argument is supplied, a ValueError is raised.
        '''
        try:
            self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                        number_of_steps=number_of_steps)
            self.assertEqual(self.widget.number_of_steps, expected_steps)
            self.assertEqual(self.widget.step_size, expected_size)
        except ValueError:
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                            number_of_steps=number_of_steps)

    @parameterized.expand([("positive", 5, 5, 400), ("negative", -10, 10, 0.1),
                           ("float", 2.5, 2, 1000), ("long", 9.99999, 9, 222)])
    def test_input_number_of_ticks(self, name, number_of_ticks, expected_ticks, expected_interval):
        '''Tests the correct widget behaviour when different 'number_of_ticks'
        arguments are supplied.
        If an invalid argument is supplied, a ValueError is raised.
        '''
        try:
            self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                        number_of_ticks=number_of_ticks)
            self.assertEqual(self.widget.number_of_ticks, expected_ticks)
            self.assertEqual(self.widget.tick_interval, expected_interval)
            self.assertEqual(self.widget.slider.tickInterval(), expected_interval)
        except ValueError:
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                            number_of_ticks=number_of_ticks)

    def test_init_default_slider(self):
        '''Tests the instantiation of the QSlider widget.
        '''
        self.assertIsInstance(self.widget.slider, QSlider)

    def test_init_default_validator(self):
        '''Tests the instantiation of the QValidator widget.
        '''
        self.assertIsInstance(self.widget.validator, QtGui.QValidator)

    def test_init_default_lineedit(self):
        '''Tests the instantiation of the QLineEdit widget.
        '''
        self.assertIsInstance(self.widget.line_edit, QLineEdit)

    def test_init_default_labels(self):
        '''Tests the instantiation of the QLabel widgets.
        '''
        self.assertIsInstance(self.widget.min_label, QLabel)
        self.assertIsInstance(self.widget.median_label, QLabel)
        self.assertIsInstance(self.widget.max_label, QLabel)

    def test_init_default_gridlayout(self):
        '''Tests the instantiation of the QGridLayout.
        '''
        self.assertIsInstance(self.widget.widget_layout, QGridLayout)

    @parameterized.expand([("positive", 0.0, 10.0, 5.0, 5.0), ("negative", -10.0, 0.0, -5.0, -5.0),
                           ("decimal", -0.5, 0.5, 0.25, 0.25),
                           ("long", -9.99999, 9.99999, 1.11111, 1.11)])
    def test_get_and_set_value(self, name, minimum, maximum, value, expected):
        '''Tests the getting and setting of the widget's 'value' property.
        '''
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
        self.widget.setValue(value)
        self.assertEqual(self.widget.getValue(), expected)

    def test_get_slider_value(self):
        '''Tests getting the QSlider value.
        '''
        self.widget.slider.setValue(50)
        self.assertEqual(self.widget._getSliderValue(), 50)

    def test_get_lineedit_value(self):
        '''Tests getting the QLineEdit value.
        '''
        self.widget.line_edit.setText("5.0")
        self.assertEqual(self.widget._getLineEditValue(), 5.0)

    def test_acceptable_update_slider(self):
        '''Tests updating the QSlider with a valid QLineEdit value.
        '''
        self.widget.line_edit.setText("10.0")
        self.widget._updateSlider()
        self.assertEqual(self.widget._getSliderValue(), 2000)
        self.assertEqual(self.widget.getValue(), 10.0)

    @parameterized.expand([("empty", "", 0, -10.0), ("lt_min", "-11.0", 0, -10.0),
                           ("gt_max", "11.0", 2000, 10.0)])
    def test_invalid_update_slider(self, name, value, expected_slider_value,
                                   expected_line_edit_value):
        '''Tests updating the QSlider with a valid QLineEdit value.
        '''
        self.widget.line_edit.setText(value)
        self.widget._updateSlider()
        self.assertEqual(self.widget._getSliderValue(), expected_slider_value)
        self.assertEqual(self.widget.getValue(), expected_line_edit_value)

    def test_update_lineedit(self):
        '''Tests updating the QLineEdit with a valid QSlider value.
        '''
        self.widget.slider.setValue(1500)
        self.widget._updateLineEdit()
        self.assertEqual(self.widget._getLineEditValue(), 5.0)

    @parameterized.expand([("positive", 5.0, 1500), ("negative", -5.0, 500), ("float", 2.5, 1250),
                           ("long", 9.99999, 1999)])
    def test_scale_lineedit_to_slider(self, name, value, expected):
        '''Tests converting a valid QLineEdit value into a scaled QSlider value.
        '''
        self.assertEqual(self.widget._scaleLineEditToSlider(value), expected)

    @parameterized.expand([("positive", 1500, 5.0), ("negative", 500, -5.0), ("float", 1250, 2.5),
                           ("long", 1999, 9.99)])
    def test_scale_slider_to_lineedit(self, name, value, expected):
        '''Tests converting a valid QSlider value into a scaled QLineEdit value.
        '''
        self.assertEqual(self.widget._scaleSliderToLineEdit(value), expected)

    def tearDown(self):
        self.form = None
