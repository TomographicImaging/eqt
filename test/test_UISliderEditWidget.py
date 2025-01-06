import unittest

# from eqt.ui import FormDialog, UISliderEditWidget, UISliderWidget
from eqt.ui.UIFormWidget import FormWidget

# from eqt.ui.UIFormWidget import FormDockWidget

# from PySide2 import QtWidgets


class UISliderEditWidget(unittest.TestCase):
    def setUp(self):
        self.form = FormWidget()

    # def _test_create_default_widget(self):
    #     uislideredit = UISliderEditWidget()
