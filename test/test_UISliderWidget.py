import unittest

from parameterized import parameterized
from qtpy import QtGui
from qtpy.QtWidgets import QGridLayout, QLabel, QLineEdit, QSlider

from eqt.ui import UISliderWidget


class TestUISliderWidget(unittest.TestCase):
    @parameterized.expand([("standard", 0.0, 10.0), ("positive", 1.0, 10.0),
                           ("negative", -10.0, -1.0), ("float", -0.5, 0.5),
                           ("long", -9.99999, 9.99999)])
    def test_init_default_widget(self, _, minimum, maximum):
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
        self.assertIsInstance(self.widget, UISliderWidget.UISliderWidget)

    @parameterized.expand([("standard", 0.0, 10.0), ("positive", 1.0, 10.0),
                           ("negative", -10.0, -1.0), ("float", -0.5, 0.5),
                           ("long", -9.99999, 9.99999)])
    def test_init_default_properties(self, _, minimum, maximum):
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
        self.assertEqual(self.widget.decimals, 2)
        self.assertEqual(self.widget.number_of_steps, 2000)
        self.assertEqual(self.widget.number_of_ticks, 10)

    @parameterized.expand([("standard", 0.0, 10.0, 5.0), ("positive", 1.0, 10.0, 5.5),
                           ("negative", -10.0, -1.0, -5.5), ("float", -0.5, 0.5, 0.0),
                           ("long", 1.11111, 9.99999, 5.5600000000000005)])
    def test_init_median(self, _, minimum, maximum, median):
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
        self.assertEqual(self.widget.median, median)

    def _test_widget_state(self):
        self.assertTrue(self.widget.isVisible())
        self.assertTrue(self.widget.isEnabled())

    @parameterized.expand([("min_gt_max", 10.0, 0.0), ("min_eq_max", 0.0, 0.0)])
    def test_input_invalid_min_max(self, _, minimum, maximum):
        with self.assertRaises(ValueError):
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)

    @parameterized.expand([("positive", 10, 10), ("negative", -10, 0), ("float", 2.5, 2),
                           ("long", 9.99999, 9)])
    def test_input_decimals(self, _, decimals, expected):
        try:
            self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0,
                                                        decimals=decimals)
            self.assertEqual(self.widget.decimals, expected)
        except ValueError:
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5,
                                                            decimals=decimals)

    @parameterized.expand([("positive", 1500, 1500, 0.013333333333333334),
                           ("negative", -50, 2000, 0.0005), ("float", 2.5, 2, 10.0),
                           ("long", 9.99999, 9, 2.2222222222222223)])
    def test_input_number_of_steps(self, _, number_of_steps, expected_steps, expected_size):
        try:
            self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0,
                                                        number_of_steps=number_of_steps)
            self.assertEqual(self.widget.number_of_steps, expected_steps)
            self.assertEqual(self.widget.step_size, expected_size)
        except ValueError:
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0,
                                                            number_of_steps=number_of_steps)

    @parameterized.expand([("positive", 5, 5, 400), ("negative", -10, 10, 0.1),
                           ("float", 2.5, 2, 1000), ("long", 9.99999, 9, 222)])
    def test_input_number_of_ticks(self, _, number_of_ticks, expected_ticks, expected_interval):
        try:
            self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0,
                                                        number_of_ticks=number_of_ticks)
            self.assertEqual(self.widget.number_of_ticks, expected_ticks)
            self.assertEqual(self.widget.tick_interval, expected_interval)
        except ValueError:
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0,
                                                            number_of_ticks=number_of_ticks)

    def test_init_default_slider(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertIsInstance(self.widget.slider, QSlider)

    def test_init_default_validator(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertIsInstance(self.widget.validator, QtGui.QValidator)

    def test_init_default_lineedit(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertIsInstance(self.widget.line_edit, QLineEdit)

    def test_init_default_labels(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertIsInstance(self.widget.min_label, QLabel)
        self.assertIsInstance(self.widget.median_label, QLabel)
        self.assertIsInstance(self.widget.max_label, QLabel)

    def test_init_default_gridlayout(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertIsInstance(self.widget.widget_layout, QGridLayout)

    @parameterized.expand([("positive", 0.0, 10.0, 5.0, 5.0), ("negative", -10.0, 0.0, -5.0, -5.0),
                           ("decimal", -0.5, 0.5, 0.25, 0.25),
                           ("long", -9.99999, 9.99999, 1.11111, 1.11111)])
    def test_get_and_set_value(self, _, minimum, maximum, value, expected):
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum)
        self.widget.setValue(value)
        self.assertEqual(self.widget.getValue(), expected)

    def test_get_slider_value(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.widget.slider.setValue(50)
        self.assertEqual(self.widget._getSliderValue(), 50)

    def test_get_lineedit_value(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.widget.line_edit.setText("5.0")
        self.assertEqual(self.widget._getLineEditValue(), 5.0)

    def test_acceptable_update_slider(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.widget.line_edit.setText("10.0")
        self.widget._updateSlider()
        self.assertEqual(self.widget._getSliderValue(), 2000)
        self.assertEqual(self.widget.getValue(), 10.0)

    def test_gt_max_update_slider(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.widget.line_edit.setText("11.0")
        self.widget._updateSlider()
        self.assertEqual(self.widget._getSliderValue(), self.widget.slider_maximum)
        self.assertEqual(self.widget.getValue(), self.widget.maximum)

    def test_invalid_update_slider(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.widget.line_edit.setText("-11.0")
        self.widget._updateSlider()
        self.assertEqual(self.widget._getSliderValue(), self.widget.slider_minimum)
        self.assertEqual(self.widget.getValue(), self.widget.minimum)

    def test_update_lineedit(self):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.widget.slider.setValue(1500)
        self.widget._updateLineEdit()
        self.assertEqual(self.widget._getLineEditValue(), 5.0)

    @parameterized.expand([("positive", 5.0, 1500), ("negative", -5.0, 500), ("float", 2.5, 1250),
                           ("long", 9.99999, 1999)])
    def test_scale_up(self, _, value, expected):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertEqual(self.widget._scaleUp(value), expected)

    @parameterized.expand([("positive", 1500, 5.0), ("negative", 500, -5.0), ("float", 1250, 2.5),
                           ("long", 1999, 9.99)])
    def test_scale_down(self, _, value, expected):
        self.widget = UISliderWidget.UISliderWidget(minimum=-10.0, maximum=10.0)
        self.assertEqual(self.widget._scaleDown(value), expected)

    def tearDown(self):
        self.form = None
