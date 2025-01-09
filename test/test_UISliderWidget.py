import unittest

from eqt.ui import UISliderWidget

# from parameterized import parameterized, parameterized_class

# from PySide2 import QtWidgets


class TestUISliderWidget(unittest.TestCase):
    def setUp(self):
        self.widget = UISliderWidget()

    def _test_init_default_widget(self):
        self.assertIsInstance(self.widget, UISliderWidget)

    def _test_init_default_properties(self):
        self.assertEqual(self.widget.minimum, 0.0)
        self.assertEqual(self.widget.maximum, 10.0)
        self.assertEqual(self.widget.step_size, 1.0)
        self.assertEqual(self.widget.scale_factor, 1.0)
        self.assertEqual(self.widget.tick_interval, 1.0)

    def _test_widget_state(self):
        self.assertTrue(self.widget.isVisible())
        self.assertTrue(self.widget.isEnabled())

    def _test_input_custom_min_max(self):
        self.widget = UISliderWidget(minimum=5.0, maximum=100.0)

        self.assertEqual(self.widget.minimum, 0.0)
        self.assertEqual(self.widget.maximum, 1.0)

    def _test_input_negative_min_max(self):
        self.widget = UISliderWidget(minimum=-1.0, maximum=0.0)

        self.assertEqual(self.widget.minimum, -1.0)
        self.assertEqual(self.widget.maximum, 0.0)

    def _test_input_invalid_min_max(self):
        ...

    def _test_input_step_size(self):
        ...

    def _test_input_scale_factor(self):
        ...

    def _test_input_tick_interval(self):
        ...

    def _test_init_default_slider(self):
        ...

    def _test_connect_slider(self):
        ...

    def _test_init_default_validator(self):
        ...

    def _test_connect_validator(self):
        ...

    def _test_init_default_lineedit(self):
        ...

    def _test_connect_lineedit(self):
        ...

    def _test_init_default_labels(self):
        ...

    def _test_init_default_gridlayout(self):
        ...

    def _test_get_value(self):
        ...

    def _test_set_value(self):
        ...

    def _test_get_slider_value(self):
        ...

    def _test_get_lineedit_value(self):
        ...

    def _test_update_slider(self):
        ...

    def _test_update_lineedit(self):
        ...

    def tearDown(self):
        self.form = None
