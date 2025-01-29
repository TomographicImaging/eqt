import sys

from qtpy import QtGui
from qtpy.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QSlider
from unittest_parametrize import ParametrizedTestCase, param, parametrize

from eqt.ui import UISliderWidget


class TestUISliderWidget(ParametrizedTestCase):
    def setUp(self):
        self.app = QApplication(sys.argv)
        self.test_widgets = {
            "standard": {"minimum": 0.0,
                         "maximum": 10.0}, "positive": {"minimum": 1.0, "maximum": 10.0},
            "negative": {"minimum": -10.0,
                         "maximum": -1.0}, "float": {"minimum": -0.5, "maximum": 0.5},
            "long": {"minimum": 1.11111, "maximum": 9.99999}}

    @parametrize(
        "expected_minimum,expected_maximum,test_widget",
        [
            param(0.0, 10.0, "standard", id="standard"),
            param(1.0, 10.0, "positive", id="positive"),
            param(-10.0, -1.0, "negative", id="negative"),
            param(-0.5, 0.5, "float", id="float"),
            param(1.11, 10.0, "long", id="long"),],
    )
    def test_init(self, expected_minimum, expected_maximum, test_widget):
        '''Tests widget instantiation using required arguments.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.assertIsInstance(self.widget, UISliderWidget.UISliderWidget)
        self.assertEqual(self.widget.minimum, expected_minimum)
        self.assertEqual(self.widget.maximum, expected_maximum)

    @parametrize(
        "minimum,maximum",
        [
            param(10.0, 0.0, id="min_gt_max"),
            param(0.0, 0.0, id="min_eq_max"),],
    )
    def test_init_invalid_min_max(self, minimum, maximum):
        '''Tests widget behaviour when invalid combinations of the required arguments are supplied.
        '''
        with self.assertRaises(ValueError):
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

    def test_init_default_attributes(self):
        '''Tests the setting of the widget's default attributes.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.assertEqual(self.widget.decimals, 2)
            self.assertEqual(self.widget.number_of_steps, 2000)
            self.assertEqual(self.widget.number_of_ticks, 10)

    @parametrize(
        "median,test_widget",
        [
            param(5.0, "standard", id="standard"),
            param(5.5, "positive", id="positive"),
            param(-5.5, "negative", id="negative"),
            param(0.0, "float", id="float"),
            param(5.56, "long", id="long"),],
    )
    def test_init_median(self, median, test_widget):
        '''Tests the calculation of the median attribute.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.assertEqual(self.widget.median, median)

    @parametrize(
        "decimals,expected",
        [
            param(1, 1, id="gt_zero_1"),
            param(10, 10, id="gt_zero_10"),],
    )
    def test_input_valid_decimals(self, decimals, expected):
        '''Tests the widget behaviour when valid 'decimals' arguments are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        decimals=decimals, is_application=False)
            self.assertEqual(self.widget.decimals, expected)

    @parametrize(
        "decimals",
        [
            param(-1, id="negative_1"),
            param(-10, id="negative_10"),
            param(0, id="eq_0"),],
    )
    def test_input_invalid_value_decimals(self, decimals):
        '''Tests the widget behaviour when invalid 'decimals' values are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                            decimals=decimals,
                                                            is_application=False)

    @parametrize(
        "decimals",
        [
            param(2.5, id="float"),
            param("10", id="string"),
            param(None, id="none"),],
    )
    def test_input_invalid_type_decimals(self, decimals):
        '''Tests the widget behaviour when invalid 'decimals' types are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            with self.assertRaises(TypeError):
                self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                            decimals=decimals,
                                                            is_application=False)

    @parametrize(
        "number_of_steps,expected_steps",
        [
            param(1, 1, id="gt_zero_1"),
            param(10, 10, id="gt_zero_10"),],
    )
    def test_input_valid_number_of_steps(self, number_of_steps, expected_steps):
        '''Tests the input of valid 'number_of_steps' arguments.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        number_of_steps=number_of_steps,
                                                        is_application=False)
            self.assertEqual(self.widget.number_of_steps, expected_steps)

    @parametrize(
        "number_of_steps",
        [
            param(-1, id="negative_1"),
            param(-10, id="negative_10"),
            param(0, id="eq_0"),],
    )
    def test_input_invalid_value_steps(self, number_of_steps):
        '''Tests the widget behaviour when invalid 'number_of_steps' values are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                            number_of_steps=number_of_steps,
                                                            is_application=False)

    @parametrize(
        "number_of_steps,expected_size,test_widget",
        [
            param(10, 1.0, "standard", id="standard"),
            param(10, 0.9, "positive", id="positive"),
            param(10, 0.9, "negative", id="negative"),
            param(10, 0.1, "float", id="float"),
            param(10, 0.889, "long", id="long"),],
    )
    def test_calculate_step_size(self, number_of_steps, expected_size, test_widget):
        '''Tests the calculation of the 'step_size' attribute.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    number_of_steps=number_of_steps,
                                                    is_application=False)
        self.assertEqual(self.widget.step_size, expected_size)

    @parametrize(
        "number_of_steps",
        [
            param(2.5, id="float"),
            param("10", id="string"),
            param(None, id="none"),],
    )
    def test_input_invalid_type_steps(self, number_of_steps):
        '''Tests the widget behaviour when invalid 'number_of_steps' types are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            with self.assertRaises(TypeError):
                self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                            number_of_steps=number_of_steps,
                                                            is_application=False)

    @parametrize(
        "number_of_ticks,expected_ticks,expected_interval",
        [
            param(1, 1, 2000, id="gt_zero_1"),
            param(10, 10, 200, id="gt_zero_10"),],
    )
    def test_input_valid_ticks(self, number_of_ticks, expected_ticks, expected_interval):
        '''Tests the widget behaviour when valid 'number_of_ticks' arguments are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        number_of_ticks=number_of_ticks,
                                                        is_application=False)
            self.assertEqual(self.widget.number_of_ticks, expected_ticks)
            self.assertEqual(self.widget.tick_interval, expected_interval)
            self.assertEqual(self.widget.slider.tickInterval(), expected_interval)

    @parametrize(
        "number_of_ticks",
        [
            param(-1, id="negative_1"),
            param(-10, id="negative_10"),
            param(0, id="eq_0"),],
    )
    def test_input_invalid_value_ticks(self, number_of_ticks):
        '''Tests the widget behaviour when invalid 'number_of_ticks' values are supplied.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            with self.assertRaises(ValueError):
                self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                            number_of_ticks=number_of_ticks,
                                                            is_application=False)

    @parametrize(
        "number_of_ticks",
        [
            param(2.5, id="float"),
            param("10", id="string"),
            param(None, id="none"),],
    )
    def test_input_invalid_type_ticks(self, number_of_ticks):
        '''Tests the widget behaviour when invalid 'number_of_ticks' types are supplied.
        If an invalid argument is supplied, a TypeError is raised.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            with self.assertRaises(TypeError):
                self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                            number_of_ticks=number_of_ticks,
                                                            is_application=False)

    def test_init_default_qslider(self):
        '''Tests the instantiation of the QSlider widget.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.assertIsInstance(self.widget.slider, QSlider)

    def test_init_default_qvalidator(self):
        '''Tests the instantiation of the QValidator widget.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.assertIsInstance(self.widget.validator, QtGui.QValidator)

    def test_init_default_qlineedit(self):
        '''Tests the instantiation of the QLineEdit widget.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.assertIsInstance(self.widget.line_edit, QLineEdit)

    def test_init_default_qlabels(self):
        '''Tests the instantiation of the QLabel widgets.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.assertIsInstance(self.widget.min_label, QLabel)
            self.assertIsInstance(self.widget.median_label, QLabel)
            self.assertIsInstance(self.widget.max_label, QLabel)

    def test_init_default_qgridlayout(self):
        '''Tests the instantiation of the QGridLayout.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.assertIsInstance(self.widget.widget_layout, QGridLayout)

    @parametrize(
        "widget_value,expected_value,test_widget",
        [
            param(5.0, 5.0, "positive", id="positive"),
            param(-5.0, -5.0, "negative", id="negative"),
            param(0.25, 0.25, "float", id="float"),
            param(5.55555, 5.55555, "long", id="long"),],
    )
    def test_get_and_set_uislider_value(self, widget_value, expected_value, test_widget):
        '''Tests the getting and setting of the UISlider value.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.widget.setValue(widget_value)
        self.assertEqual(self.widget.value(), expected_value)

    def test_get_and_set_qslider_value(self):
        '''Tests the getting and setting of the QSlider value.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.widget.slider.setValue(50)
            self.assertEqual(self.widget._getQSliderValue(), 50)

    @parametrize(
        "line_edit_value,expected",
        [
            param("5.0", "5.0", id="positive"),
            param("-5.0", "-5.0", id="negative"),
            param("0.25", "0.25", id="float"),
            param("5.55555", "5.55555", id="long"),],
    )
    def test_get_and_set_qlineedit_value(self, line_edit_value, expected):
        '''Tests the getting and setting of the QLineEdit value.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.widget.line_edit.setText(line_edit_value)
            self.assertEqual(self.widget._getQLineEditValue(), expected)

    @parametrize(
        "line_edit_value,expected_slider_value,expected_line_edit_value,test_widget",
        [
            param("5.0", 888, 5.0, "positive", id="positive"),
            param("-5.0", 1111, -5.0, "negative", id="negative"),
            param("0.25", 1500, 0.25, "float", id="float"),
            param("5.55555", 1000, 5.55555, "long", id="long"),],
    )
    def test_acceptable_update_qslider(self, line_edit_value, expected_slider_value,
                                       expected_line_edit_value, test_widget):
        '''Tests updating the QSlider with a valid QLineEdit value.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.widget.line_edit.setText(line_edit_value)
        self.widget._updateQSlider()
        self.assertEqual(self.widget._getQSliderValue(), expected_slider_value)
        self.assertEqual(self.widget.value(), expected_line_edit_value)

    def test_empty_update_qslider(self):
        '''Tests updating the QSlider with an empty string QLineEdit value.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            self.widget.line_edit.setText("")
            self.widget._updateQSlider()

            self.assertEqual(self.widget._getQSliderValue(), self.widget.slider_minimum)
            self.assertEqual(self.widget.value(), self.widget.minimum)

    def test_lt_min_update_qslider(self):
        '''Tests updating the QSlider with a QLineEdit value less than the minimum.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            lt_min_value = str(minimum - 1)
            self.widget.line_edit.setText(lt_min_value)

            with self.assertRaises(ValueError):
                self.widget._updateQSlider()

            self.assertEqual(self.widget._getQSliderValue(), self.widget.slider_minimum)
            self.assertEqual(self.widget.value(), self.widget.minimum)

    def test_gt_max_update_qslider(self):
        '''Tests updating the QSlider with a QLineEdit value greater than the maximum.
        '''
        for params in self.test_widgets.values():
            minimum = params.get("minimum")
            maximum = params.get("maximum")
            self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                        is_application=False)

            gt_min_value = str(maximum + 1)
            self.widget.line_edit.setText(gt_min_value)

            with self.assertRaises(ValueError):
                self.widget._updateQSlider()

            self.assertEqual(self.widget._getQSliderValue(), self.widget.slider_maximum)
            self.assertEqual(self.widget.value(), self.widget.maximum)

    @parametrize(
        "slider_value,expected_line_edit_value,test_widget",
        [
            param(888, "5.0", "positive", id="positive"),
            param(1111, "-5.0", "negative", id="negative"),
            param(1500, "0.25", "float", id="float"),
            param(1000, "5.56", "long", id="long"),],
    )
    def test_update_qlineedit(self, slider_value, expected_line_edit_value, test_widget):
        '''Tests updating the QLineEdit with a valid QSlider value.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.widget.slider.setValue(slider_value)
        self.widget._updateQLineEdit()
        self.assertEqual(self.widget._getQLineEditValue(), expected_line_edit_value)

    @parametrize(
        "line_edit_value,expected,test_widget",
        [
            param(5.0, 888, "positive", id="positive"),
            param(-5.0, 1111, "negative", id="negative"),
            param(2.5, 6000, "float", id="float"),
            param(9.99999, 1999, "long", id="long"),],
    )
    def test_scale_lineedit_to_slider(self, line_edit_value, expected, test_widget):
        '''Tests converting a valid QLineEdit value into a scaled QSlider value.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.assertEqual(self.widget._scaleLineEditToSlider(line_edit_value), expected)

    @parametrize(
        "slider_value,expected,test_widget",
        [
            param(1000, 5.5, "positive", id="positive"),
            param(1000, -5.5, "negative", id="negative"),
            param(1000, 0.0, "float", id="float"),
            param(1000, 5.56, "long", id="long"),],
    )
    def test_scale_slider_to_lineedit(self, slider_value, expected, test_widget):
        '''Tests converting a valid QSlider value into a scaled QLineEdit value.
        '''
        minimum = self.test_widgets.get(test_widget).get("minimum")
        maximum = self.test_widgets.get(test_widget).get("maximum")
        self.widget = UISliderWidget.UISliderWidget(minimum=minimum, maximum=maximum,
                                                    is_application=False)

        self.assertEqual(self.widget._scaleSliderToLineEdit(slider_value), expected)

    def tearDown(self):
        self.form = None
        sys.exit(self.app.exec_())
