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
        '''Tests widget instantiation using 'minimum'/'maximum' arguments.
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
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            self.assertEqual(widget.decimals, 2)
            self.assertEqual(widget.number_of_steps, 2000)
            self.assertEqual(widget.number_of_ticks, 10)

    @parameterized.expand([("standard", 5.0), ("positive", 5.5), ("negative", -5.5),
                           ("float", 0.0), ("long", 5.56)])
    def test_init_median(self, _, median):
        '''Tests the calculation of the 'median' property.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

        self.assertEqual(widget.median, median)

    def test_widget_state(self):
        '''Tests default widget states.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

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
                           ("long", 9.99999, 9), ("value", "10", 10)])
    def test_input_decimals(self, _, decimals, expected):
        '''Tests the correct widget behaviour when different 'decimals'
        arguments are supplied.
        If an invalid argument is supplied, a ValueError is raised.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")

            try:
                widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                       decimals=decimals)
                self.assertEqual(widget.decimals, expected)
            except (ValueError, TypeError) as error:
                with self.assertRaises(error):
                    widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                           decimals=decimals)

    @parameterized.expand([("positive", 1500, 1500, 0.006), ("negative", -50, 2000, 0.0005),
                           ("float", 2.5, 2, 0.5), ("long", 9.99999, 9, 0.9877777777777779)])
    def test_input_number_of_steps(self, _, number_of_steps, expected_steps, expected_size):
        '''Tests the correct widget behaviour when different 'number_of_steps'
        arguments are supplied.
        If an invalid argument is supplied, a ValueError is raised.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")

        try:
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                   number_of_steps=number_of_steps)
            self.assertEqual(widget.number_of_steps, expected_steps)
            self.assertEqual(widget.step_size, expected_size)
        except (ValueError, TypeError) as error:
            with self.assertRaises(error):
                widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                       number_of_steps=number_of_steps)

    @parameterized.expand([("positive", 5, 5, 400), ("negative", -10, 10, 0.1),
                           ("float", 2.5, 2, 1000), ("long", 9.99999, 9, 222)])
    def test_input_number_of_ticks(self, _, number_of_ticks, expected_ticks, expected_interval):
        '''Tests the correct widget behaviour when different 'number_of_ticks'
        arguments are supplied.
        If an invalid argument is supplied, a ValueError is raised.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")

            try:
                widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                       number_of_ticks=number_of_ticks)
                self.assertEqual(widget.number_of_ticks, expected_ticks)
                self.assertEqual(widget.tick_interval, expected_interval)
                self.assertEqual(widget.slider.tickInterval(), expected_interval)
            except (ValueError, TypeError) as error:
                with self.assertRaises(error):
                    widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                           number_of_ticks=number_of_ticks)

    def test_init_default_slider(self):
        '''Tests the instantiation of the QSlider widget.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            self.assertIsInstance(widget.slider, QSlider)

    def test_init_default_validator(self):
        '''Tests the instantiation of the QValidator widget.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            self.assertIsInstance(widget.validator, QtGui.QValidator)

    def test_init_default_lineedit(self):
        '''Tests the instantiation of the QLineEdit widget.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            self.assertIsInstance(widget.line_edit, QLineEdit)

    def test_init_default_labels(self):
        '''Tests the instantiation of the QLabel widgets.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            self.assertIsInstance(widget.min_label, QLabel)
            self.assertIsInstance(widget.median_label, QLabel)
            self.assertIsInstance(widget.max_label, QLabel)

    def test_init_default_gridlayout(self):
        '''Tests the instantiation of the QGridLayout.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            self.assertIsInstance(widget.widget_layout, QGridLayout)

    @parameterized.expand([("positive", 5.0, 5.0), ("negative", -5.0, -5.0), ("float", 0.25, 0.25),
                           ("long", 5.55555, 5.55555)])
    def test_get_and_set_value(self, _, widget_value, expected):
        '''Tests the getting and setting of the widget's 'value' property.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

        widget.setValue(widget_value)
        self.assertEqual(widget.value(), expected)

    def test_get_slider_value(self):
        '''Tests getting the QSlider value.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            widget.slider.setValue(50)
            self.assertEqual(widget._getSliderValue(), 50)

    @parameterized.expand([("positive", "5.0", "5.0"), ("negative", "-5.0", "-5.0"),
                           ("float", "0.25", "0.25"), ("long", "5.55555", "5.55555")])
    def test_get_lineedit_value(self, _, line_edit_value, expected):
        '''Tests getting the QLineEdit value.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            widget.line_edit.setText(line_edit_value)
            self.assertEqual(widget._getLineEditValue(), expected)

    @parameterized.expand([("positive", "5.0", 888, 5.0), ("negative", "-5.0", 1111, -5.0),
                           ("float", "0.25", 1500, 0.25), ("long", "5.55555", 1000, 5.55555)])
    def test_acceptable_update_slider(self, _, line_edit_value, expected_slider_value,
                                      expected_line_edit_value):
        '''Tests updating the QSlider with a valid QLineEdit value.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

        widget.line_edit.setText(line_edit_value)
        widget._updateSlider()
        self.assertEqual(widget._getSliderValue(), expected_slider_value)
        self.assertEqual(widget.value(), expected_line_edit_value)

    @parameterized.expand([("empty", "", 0), ("lt_min", "-11.0", 0), ("gt_max", "11.0", 2000)])
    def test_invalid_update_slider(self, _, line_edit_value, expected_slider_value):
        '''Tests updating the QSlider with a valid QLineEdit value.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

            widget.line_edit.setText(line_edit_value)
            widget._updateSlider()
            self.assertEqual(widget._getSliderValue(), expected_slider_value)
            if _ == "gt_max":
                self.assertEqual(widget.value(), widget.maximum)
            elif _ == "empty" or "lt_min":
                self.assertEqual(widget.value(), widget.minimum)

    @parameterized.expand([("positive", 888, 5.0), ("negative", 1111, -5.0), ("float", 1500, 0.25),
                           ("long", 1000, 5.56)])
    def test_update_lineedit(self, _, slider_value, expected_line_edit_value):
        '''Tests updating the QLineEdit with a valid QSlider value.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

        widget.slider.setValue(slider_value)
        widget._updateLineEdit()
        self.assertEqual(widget._getLineEditValue(), expected_line_edit_value)

    @parameterized.expand([("positive", 5.0, 888), ("negative", -5.0, 1111), ("float", 2.5, 6000),
                           ("long", 9.99999, 1999)])
    def test_scale_lineedit_to_slider(self, _, line_edit_value, expected):
        '''Tests converting a valid QLineEdit value into a scaled QSlider value.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

        self.assertEqual(widget._scaleLineEditToSlider(line_edit_value), expected)

    @parameterized.expand([("positive", 1000, 5.5), ("negative", 1000, -5.5), ("float", 1000, 0.0),
                           ("long", 1000, 5.56)])
    def test_scale_slider_to_lineedit(self, _, slider_value, expected):
        '''Tests converting a valid QSlider value into a scaled QLineEdit value.
        '''
        minimum = self.test_widgets.get(_).get("minimum")
        maximum = self.test_widgets.get(_).get("maximum")
        widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

        self.assertEqual(widget._scaleSliderToLineEdit(slider_value), expected)

    def tearDown(self):
        self.form = None
