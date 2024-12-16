import sys

from PySide2 import QtWidgets

from eqt.ui import FormDialog, UISliderWidget


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
        uislider = UISliderWidget.UISliderWidget(dspinbox)

        # finally add to the form widget
        dialog.addWidget(uislider, 'Slider 1', 'input_slider')
        dialog.addWidget(dspinbox, '', 'input_dspinbox')

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected
        dialog.exec()

    def accepted(self):
        print("accepted")
        print(self.dialog.widgets['input_slider_field'].value())
        print(self.dialog.widgets['input_dspinbox_field'].value())
        self.dialog.close()

    def rejected(self):
        print("rejected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
