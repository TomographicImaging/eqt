import sys

from qtpy import QtWidgets

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

        # Create UISliderWidget
        uislider = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5, decimals=10,
                                                 number_of_steps=10, number_of_ticks=10)

        # add to the form widget
        dialog.addWidget(uislider, 'UISlider:', 'input_slider')

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected
        dialog.exec()

    def accepted(self):
        print("accepted")
        print(f"UISlider QSlider: {self.dialog.widgets['input_slider_field']._getSliderValue()}")
        print(f"UISlider QLineEdit: {self.dialog.widgets['input_slider_field'].getValue()}")

        self.dialog.close()

    def rejected(self):
        print("rejected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
