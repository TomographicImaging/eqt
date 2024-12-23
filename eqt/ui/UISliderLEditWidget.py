from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QGridLayout, QLabel, QLineEdit, QSlider, QWidget


class UISliderLEditWidget(QWidget):
    '''Creates a QGridLayout that includes a QSlider, min/max QLabels and a QLineEdit.
    The QLineEdit is updated with the value of the slider and vice versa.

    Parameters
    ----------
    min : float
    max : float
    step_size : float
    scale_factor : float
    '''
    def __init__(self, minimum=0.0, maximum=1.0, step_size=1.0, scale_factor=1.0):
        QWidget.__init__(self)

        self.minimum = minimum
        self.maximum = maximum
        self.scale_factor = scale_factor
        self.step_size = step_size
        self.tick_interval = self.step_size * self.scale_factor

        # Configure the QSlider
        self.slider = QSlider()
        self.slider.setRange(self.minimum, self.maximum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setSingleStep(self.step_size)
        self.slider.setTickInterval(self.step_size)

        # Connect the QSlider to the QLineEdit
        self.slider.sliderPressed.connect(self.update_line_edit)
        self.slider.sliderMoved.connect(self.update_line_edit)
        self.slider.sliderReleased.connect(self.update_line_edit)

        # Configure the QDoubleValidator and QLineEdit
        self.validator = QtGui.QDoubleValidator()
        self.validator.setBottom(self.minimum)
        self.validator.setTop(self.maximum)
        self.validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.validator.setLocale(QtCore.QLocale("en_US"))

        self.line_edit = QLineEdit()
        self.line_edit.setValidator(self.validator)
        self.line_edit.setText(str(minimum))
        self.line_edit.setPlaceholderText(str(minimum))

        # Connect the QLineEdit to the QSlider
        self.line_edit.textEdited.connect(self.update_slider)
        self.line_edit.returnPressed.connect(self.update_slider)

        # Configure the min/max QLabels
        self.min_label = QLabel()
        self.min_label.setText(str(self.minimum))
        self.max_label = QLabel()
        self.max_label.setText(str(self.maximum))

        # Configure the QGridLayout
        widget_layout = QGridLayout()
        widget_layout.addWidget(self.slider, 0, 0, 1, -1)
        widget_layout.addWidget(self.min_label, 1, 0, QtCore.Qt.AlignLeft)
        widget_layout.addWidget(self.max_label, 1, 1, QtCore.Qt.AlignRight)
        widget_layout.addWidget(self.line_edit, 2, 0, 1, -1)

        # Set the layout
        self.setLayout(widget_layout)
        self.show()

    def get_slider_value(self):
        return self.slider.value()

    def get_line_edit_value(self):
        return self.line_edit.text()

    def update_slider(self):
        state = self.validator.validate(self.line_edit.text(), 0)
        if state[0] == QtGui.QDoubleValidator.Acceptable:
            line_edit_value = float(self.get_line_edit_value())
            self.slider.setValue(line_edit_value)
        else:
            self.line_edit.setText(str(self.minimum))
            line_edit_value = float(self.get_line_edit_value())
            self.slider.setValue(line_edit_value)

    def update_line_edit(self):
        slider_value = str(float(self.get_slider_value()))
        self.line_edit.setText(slider_value)
