from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QSlider


class UISliderWidget(QSlider):
    '''Creates a Slider widget which updates
    a QLineEdit with its value (which may be scaled
    to a non-integer value by setting the scale_factor)
    Also accepts a QLabel that is configured to
    display the maximum value of the QSlider

    Parameters
    ----------
    line_edit : QLineEdit
    max_label : QLabel
    minimum : float
    maximum : float
    step_size : float
    scale_factor : float
    '''
    def __init__(self, line_edit, max_label, minimum=0.0, maximum=1.0, scale_factor=1.0,
                 step_size=1.0, tick_interval=1.0):
        QSlider.__init__(self)

        self.line_edit = line_edit
        self.max_label = max_label
        self.minimum = minimum
        self.maximum = maximum
        self.scale_factor = scale_factor
        self.step_size = step_size * self.scale_factor
        self.tick_interval = tick_interval * self.scale_factor

        # Configure the QSlider
        self.setRange(self.minimum, self.maximum)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setTickPosition(QSlider.TicksBelow)
        self.setSingleStep(self.step_size)
        self.setTickInterval(self.tick_interval)

        # Connect the QSlider to the QLineEdit
        self.sliderPressed.connect(self.updateLineEdit)
        self.sliderMoved.connect(self.updateLineEdit)
        self.sliderReleased.connect(self.updateLineEdit)

        # Configure the QDoubleValidator and QLineEdit
        self.validator = QtGui.QDoubleValidator()
        self.validator.setBottom(self.minimum)
        self.validator.setTop(self.maximum)
        self.validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.validator.setLocale(QtCore.QLocale("en_US"))

        self.line_edit.setValidator(self.validator)
        self.line_edit.setText(str(self.minimum))
        self.line_edit.setPlaceholderText(str(self.minimum))

        # Connect the QLineEdit to the QSlider
        self.line_edit.textEdited.connect(self.updateSlider)
        self.line_edit.returnPressed.connect(self.updateSlider)

        # Configure QLabel to show maximum QSlider value
        self.max_label = max_label
        self.max_label.setAlignment(QtCore.Qt.AlignRight)
        self.max_label.setText(str(self.maximum))

    def getValue(self):
        return self.getLineEditValue()

    def getSliderValue(self):
        return self.value()

    def getLineEditValue(self):
        return float(self.line_edit.text())

    def updateSlider(self):
        state = self.validator.validate(self.line_edit.text(), 0)
        if state[0] == QtGui.QDoubleValidator.Acceptable:
            line_edit_value = self.getLineEditValue()
            self.setValue(line_edit_value)
        else:
            self.line_edit.setText(str(self.minimum))
            line_edit_value = self.getLineEditValue()
            self.setValue(line_edit_value)

    def updateLineEdit(self):
        slider_value = str(float(self.getSliderValue()))
        self.line_edit.setText(slider_value)
