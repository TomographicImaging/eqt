from PySide2 import QtTest

import os
import sys
import unittest
from unittest import mock

from eqt.ui.FormDialog import FormDialog
from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication, QPushButton
from eqt.ui.UISliderWidget import UISliderWidget


app = QApplication(sys.argv)


class FormDialogStatusTest(unittest.TestCase):

    # @mock.patch("ccpi.web_viewer.trame_viewer.vtk")
    # @mock.patch("ccpi.web_viewer.trame_viewer.TrameViewer.update_slice_data")
    # def setUp(self, _, vtk_module):
    #     # Get the head data
    #     self.head_path = os.path.join(sys.prefix, 'share', 'cil', 'head.mha')
    #     self.file_list = [self.head_path, "other_file_path_dir/other_file"]

    #     # add the cil_viewer and defaults for a default __init__
    #     self.cil_viewer = mock.MagicMock()
    #     self.map_range = [0, 3790]
    #     self.cil_viewer.getSliceMapRange.return_value = self.map_range

    #     self.trame_viewer = TrameViewer(self.cil_viewer, self.file_list)

    #     # Assert on the mocks/patched objects after __init__
    #     vtk_module.VtkRemoteView.assert_called_once_with(self.cil_viewer.renWin, trame_server=server, ref="view")

    def setUp(self):
        
        self.form = FormDialog()
        self.form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
        self.form.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')
        self.form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
        self.form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
        self.form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
        self.form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
        self.form.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISliderWidget: ', 'uiSliderWidget')
        self.form.addWidget(QtWidgets.QRadioButton('test'), 'RadioButton: ', 'radioButton')
        self.form.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
        self.form.addWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: ', 'plainTextEdit')
        self.form.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')
        self.form.addWidget(QtWidgets.QPushButton('test'), 'Button: ', 'button')
        

    def test_visibility_of_widget_saved_to_state(self):
        # Check that the visibility of the widget is saved to the state
        # Have to use magic mock as we can't set the visibility of the QLabel
        # to be True, because the FormDialog is not visible
        initial_label_visibility = True
        self.form.getWidget('label').isVisible = mock.MagicMock()
        self.form.getWidget('label').isVisible.return_value = initial_label_visibility

        # TODO: should we specify whether field or label?
        
        self.assertEqual(self.form.getWidgetState('label_field')['label_field']['visible'], initial_label_visibility)

        final_label_visibility = False
        self.form.getWidget('label').isVisible.return_value = False

        self.assertEqual(self.form.getWidgetState('label_field')['label_field']['visible'], final_label_visibility)

    def test_enabled_state_of_widget_saved_to_state(self):
        # Check that the enabled state of the widget is saved to the state
        
        initial_label_enabled_state = True

        # TODO: should we specify whether field or label?
        
        self.assertEqual(self.form.getWidgetState('label_field')['label_field']['enabled'], initial_label_enabled_state)

        self.form.getWidget('label').setEnabled(False)
        final_label_enabled_state = False

        self.assertEqual(self.form.getWidgetState('label_field')['label_field']['enabled'], final_label_enabled_state)

    def test_value_of_QLabel_saved_to_state(self):
        # Check that the value of the QLabel is saved to the state
        
        initial_label_value ='test label'

        # TODO: should we specify whether field or label?
        
        self.assertEqual(self.form.getWidgetState('label_field')['label_field']['value'], initial_label_value)

        final_label_value = 'final test label'
        self.form.getWidget('label').setText(final_label_value)
        
        self.assertEqual(self.form.getWidgetState('label_field')['label_field']['value'], final_label_value)


if __name__ == "__main__":
    unittest.main()