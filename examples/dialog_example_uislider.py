import sys

from qtpy import QtWidgets

from eqt.ui import FormDialog, UISliderWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        '''Creates a QMainWindow and adds a QPushButton. Pressing the button opens a FormDialog
        containing a UISliderWidget example. The UISliderWidget is connected to a method
        that prints the current value of it's QSlider, QLineEdit, and the value of the
        UISliderWidget itself (i.e. the value returned when it's value() method is called).
        '''
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Dialog with form layout")
        pb.clicked.connect(lambda: self._openFormDialog())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)
        self.show()

    def _openFormDialog(self):
        '''Creates a FormDialog and adds a UISliderWidget. Connects signals from the widget's
        QSlider and QLineEdit to a method than prints the UISliderWidget's values. The values
        will be printed when either; the QSlider is released, or the QLineEdit is edited.
        Displays the FormDialog.
        '''
        dialog = FormDialog(parent=self, title='UISliderWidget Example')
        uislider = UISliderWidget.UISliderWidget(minimum=-0.5, maximum=0.5, decimals=10,
                                                 number_of_steps=10, number_of_ticks=10)
        dialog.addWidget(uislider, 'UISlider:', 'input_slider')

        dialog.widgets['input_slider_field'].slider.sliderReleased.connect(
            lambda: self._printValues())
        dialog.widgets['input_slider_field'].line_edit.editingFinished.connect(
            lambda: self._printValues())

        self.dialog = dialog
        dialog.exec()

    def _printValues(self):
        '''Prints the values of the QSlider, QLineEdit and the UISliderWidget itself.
        Also prints the type of each value.
        '''
        slider_value = self.dialog.widgets['input_slider_field']._getQSliderValue()
        line_edit_value = self.dialog.widgets['input_slider_field']._getQLineEditValue()
        uislider_value = self.dialog.widgets['input_slider_field'].value()
        print(f"QSlider Value: {slider_value} {type(slider_value)}\n" +
              f"QLineEdit Value: {line_edit_value} {type(line_edit_value)}\n" +
              f"UISliderWidget Value: {uislider_value} {type(uislider_value)}\n")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
