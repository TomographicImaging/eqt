from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QGridLayout, QLabel, QLineEdit, QSlider, QWidget


class UISliderEditWidget(QWidget):
    '''Creates a QGridLayout that includes a QSlider, min/median/max QLabels and a QLineEdit.
    The QLineEdit is updated with the value of the slider and vice versa.

    Parameters
    ----------
    min : float
    max : float
    step_size : float
    scale_factor : float
    tick_interval : float
    '''
    def __init__(self, minimum=0.0, maximum=10.0, step_size=1.0, scale_factor=1.0,
                 tick_interval=1.0):
        QWidget.__init__(self)

        self.minimum = minimum
        self.maximum = maximum
        self.scale_factor = scale_factor
        self.step_size = step_size * self.scale_factor
        self.tick_interval = tick_interval * self.scale_factor

        # Configure the QSlider
        self.slider = QSlider()
        self.slider.setRange(self.minimum, self.maximum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setSingleStep(self.step_size)
        self.slider.setTickInterval(self.tick_interval)

        # Connect the QSlider to the QLineEdit
        self.slider.sliderPressed.connect(self.updateLineEdit)
        self.slider.sliderMoved.connect(self.updateLineEdit)
        self.slider.sliderReleased.connect(self.updateLineEdit)

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
        self.line_edit.textEdited.connect(self.updateSlider)
        self.line_edit.returnPressed.connect(self.updateSlider)

        # Configure QLabels
        self.min_label = QLabel()
        self.min_label.setText(str(self.minimum))
        self.median_label = QLabel()
        self.median_label.setText(str(self.maximum * 0.5))
        self.max_label = QLabel()
        self.max_label.setText(str(self.maximum))

        # Configure quartile QLabels
        # self.lowerq_label = QLabel()
        # self.lowerq_label.setText(str(self.maximum * 0.25))
        # self.upperq_label = QLabel()
        # self.upperq_label.setText(str(self.maximum * 0.75))

        # Configure the QGridLayout
        widget_layout = QGridLayout()
        widget_layout.addWidget(self.slider, 0, 0, 1, -1)
        widget_layout.addWidget(self.min_label, 1, 0, QtCore.Qt.AlignLeft)
        # widget_layout.addWidget(self.lowerq_label, 1, 1, QtCore.Qt.AlignLeft)
        widget_layout.addWidget(self.median_label, 1, 1, QtCore.Qt.AlignCenter)
        # widget_layout.addWidget(self.upperq_label, 1, 3, QtCore.Qt.AlignRight)
        widget_layout.addWidget(self.max_label, 1, 2, QtCore.Qt.AlignRight)
        widget_layout.addWidget(self.line_edit, 2, 0, 1, -1)

        # Set the layout
        self.setLayout(widget_layout)
        self.show()

    def getValue(self):
        return self.getLineEditValue()

    def setValue(self, value):
        self.line_edit.setText(str(value))

    def getSliderValue(self):
        return self.slider.value()

    def getLineEditValue(self):
        return float(self.line_edit.text())

    def updateSlider(self):
        state = self.validator.validate(self.line_edit.text(), 0)
        if state[0] == QtGui.QDoubleValidator.Acceptable:
            line_edit_value = self.getLineEditValue()
            self.slider.setValue(line_edit_value)
            self.setValue(line_edit_value)
        else:
            self.line_edit.setText(str(self.minimum))
            line_edit_value = self.getLineEditValue()
            self.slider.setValue(line_edit_value)
            self.setValue(line_edit_value)

    def updateLineEdit(self):
        slider_value = str(float(self.getSliderValue()))
        self.line_edit.setText(slider_value)
