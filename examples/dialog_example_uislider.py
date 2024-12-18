import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UISliderLineEditWidget, UISliderWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with form layout")
        pb.clicked.connect(lambda: self.openFormDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        self.show()

    def openFormDialog(self):
        dialog = FormDialog(parent=self, title='Example')
        dialog.Ok.clicked.connect(lambda: self.accepted())

        # Example on how to add elements to the FormDialog
        # add input 1 as UISliderWidget and DoubleSpinBox
        dspinbox = QtWidgets.QDoubleSpinBox()
        min_label = QtWidgets.QLabel()
        max_label = QtWidgets.QLabel()
        uislider = UISliderWidget.UISliderWidget(dspinbox, min_label, max_label, minimum=0.00,
                                                 maximum=10.00, step_size=1.00)

        # add to the form widget
        dialog.addWidget(uislider, 'QSlider 1:', 'input_slider1')
        dialog.addWidget(dspinbox, '', 'input_dspinbox1')

        # add input 2 as UISliderLineEditWidget
        dspinbox = QtWidgets.QDoubleSpinBox()
        uislider = UISliderLineEditWidget.UISliderLineEditWidget(minimum=0.00, maximum=10.00,
                                                                 step_size=2.00)

        # add to the form widget
        dialog.addWidget(uislider, 'QSlider 2:', 'input_slider2')

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected
        dialog.exec()

    def accepted(self):
        print("accepted")
        print(f"QSlider 1 Value: {self.dialog.widgets['input_slider1_field'].value()}")
        print(f"QDoubleSpinBox 1 Value: {self.dialog.widgets['input_dspinbox1_field'].value()}")

        print(f"QSlider 2 Value: {self.dialog.widgets['input_slider2_field'].value()}")

        self.dialog.close()

    def rejected(self):
        print("rejected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
