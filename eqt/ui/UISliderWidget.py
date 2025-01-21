from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QSlider, QWidget


class UISliderWidget(QWidget):
    '''Creates a QGridLayout that includes a QSlider, min/median/max QLabels and a QLineEdit.
    Updating a widget scales the value appropriately for the other widget,
    i.e. the QLineEdit is updated with the value of the slider and vice versa.

    Parameters
    ----------
    minimum : float
        - Minimum value of the QLineEdit
    maximum : float
        - Maximum value of the QLineEdit
    decimals : int
        - Number of decimal places that the QLabels, QLineEdit and QSlider steps can display
    number_of_steps : int
        - Number of steps in the QSlider
    number_of_ticks : int
        - Number of ticks visualised under the QSlider, determines tick interval
    '''
    def __init__(self, minimum, maximum, decimals=2, number_of_steps=2000, number_of_ticks=10):
        QWidget.__init__(self)

        # Check that the minimum/maximum arguments are valid
        if minimum >= maximum:
            raise ValueError("'minimum' argument must be less than 'maximum'")

        self._setDecimals(decimals)
        self._setNumberOfSteps(number_of_steps)
        self._setNumberOfTicks(number_of_ticks)

        self.minimum = round(minimum, self.decimals)
        self.maximum = round(maximum, self.decimals)
        self.median = round(((self.maximum - self.minimum) / 2), self.decimals) + self.minimum

        self.slider_minimum = 0
        self.slider_maximum = self.number_of_steps

        self.step_size = float((self.maximum - self.minimum) / self.number_of_steps)
        self.tick_interval = round(
            (self.slider_maximum - self.slider_minimum) / self.number_of_ticks)

        # Configure the QSlider
        self.slider = QSlider()
        self.slider.setRange(self.slider_minimum, self.slider_maximum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(self.tick_interval)

        # Connect the QSlider to the QLineEdit
        self.slider.valueChanged.connect(self._updateLineEdit)

        # Configure the QDoubleValidator and QLineEdit
        self.validator = QtGui.QDoubleValidator()
        self.validator.setBottom(self.minimum)
        self.validator.setTop(self.maximum)
        self.validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.validator.setLocale(QtCore.QLocale("en_US"))

        self.line_edit = QLineEdit()
        self.line_edit.setValidator(self.validator)
        self.line_edit.setText(str(self.minimum))
        self.line_edit.setPlaceholderText(str(self.minimum))

        # Connect the QLineEdit to the QSlider
        self.line_edit.editingFinished.connect(self._updateSlider)
        self.line_edit.returnPressed.connect(self._updateSlider)

        # Configure the QApplication
        self.app = QApplication.instance()

        # Connect the QApplication to the QLineEdit
        self.app.focusChanged.connect(self._updateSlider)

        # Configure QLabels
        self.min_label = QLabel()
        self.min_label.setText(str(self.minimum))
        self.median_label = QLabel()
        self.median_label.setText(str(self.median))
        self.max_label = QLabel()
        self.max_label.setText(str(self.maximum))

        # Configure the QGridLayout
        self.widget_layout = QGridLayout()
        self.widget_layout.addWidget(self.slider, 0, 0, 1, -1)
        self.widget_layout.addWidget(self.min_label, 1, 0, QtCore.Qt.AlignLeft)
        self.widget_layout.addWidget(self.median_label, 1, 1, QtCore.Qt.AlignCenter)
        self.widget_layout.addWidget(self.max_label, 1, 2, QtCore.Qt.AlignRight)
        self.widget_layout.addWidget(self.line_edit, 2, 0, 1, -1)

        # Set the layout
        self.setLayout(self.widget_layout)
        self.show()

    def getValue(self):
        '''Gets the value of the UISliderWidget, which is the same as the QLineEdit value.
        This method is called by methods in the UIFormWidget class responsible for
        saving widget states, maintaining the naming convention used by other QWidgets.
        '''
        return self._getLineEditValue()

    def setValue(self, value):
        '''Sets the value of the UISliderWidget, which is the same as the QLineEdit value.
        This method is called by methods in the UIFormWidget class responsible for
        applying/loading widget states, maintaining the naming convention used by other QWidgets.

        Parameters
        ----------
        value : float
        '''
        self.line_edit.setText(str(value))
        self.slider.setValue(self._scaleLineEditToSlider(self._getLineEditValue()))

    def _setDecimals(self, decimals):
        '''Sets the number of decimal places that the QLabels, QLineEdit and
        QSlider steps can display. Also checks that the argument provided is valid,
        i.e. that it is a positive integer value - if the value is invalid, the method raises
        a ValueError during object instantiation.

        Parameters
        ----------
        decimals : int
        '''
        if decimals < 0:
            raise ValueError("'decimals' value must be a positive integer")
        else:
            self.decimals = int(decimals)

    def _setNumberOfSteps(self, number_of_steps):
        '''Sets the number of steps in the QSlider. Steps are each subdivision of the
        QSlider's range. Also checks that the argument provided is valid, i.e. that
        it is a positive integer value - if the value is invalid, the method raises
        a ValueError during object instantiation.

        Parameters
        ----------
        number_of_steps : int
        '''
        if number_of_steps < 0:
            raise ValueError("'number_of_steps' value must be a positive integer")
        else:
            self.number_of_steps = int(number_of_steps)

    def _setNumberOfTicks(self, number_of_ticks):
        '''Sets the number of ticks that the QSlider displays. Ticks are the notches
        displayed underneath the QSlider. Also checks that the argument provided is
        valid, i.e. that it is a positive integer value - if the value is invalid,
        the method raises a ValueError during object instantiation.

        Parameters
        ----------
        number_of_ticks : int
        '''
        if number_of_ticks < 0:
            raise ValueError("'number_of_ticks' value must be a positive integer")
        else:
            self.number_of_ticks = int(number_of_ticks)

    def _getSliderValue(self):
        '''Gets the current value of the QSlider, returning either 0 or a positive integer.
        '''
        return self.slider.value()

    def _getLineEditValue(self):
        '''Gets the current value of the QLineEdit. If the QLineEdit is empty,
        this method returns the UISliderWidget's minimum value - otherwise, it
        returns a float value between the UISliderWidget's minimum and maximum values.
        '''
        if self.line_edit.text() == '':
            return self.minimum
        else:
            return float(self.line_edit.text())

    def _updateSlider(self):
        '''Updates the QSlider to reflect the current value of the QLineEdit.
        The method uses the state of the QValidator to check that the QLineEdit
        value is valid - if it is valid, it sets the value of the QSlider to the
        scaled value of the QLineEdit. Otherwise, it will update the QSlider with
        either the scaled value of the QLineEdit's minimum or maximum.
        '''
        line_edit_value = self._getLineEditValue()
        state = self.validator.validate(self.line_edit.text(), 0)
        if state[0] == QtGui.QDoubleValidator.Acceptable:
            self.slider.setValue(self._scaleLineEditToSlider(line_edit_value))
            self.setValue(line_edit_value)
        elif line_edit_value > self.maximum:
            self.line_edit.setText(str(self.maximum))
            line_edit_value = self._getLineEditValue()
            self.slider.setValue(self._scaleLineEditToSlider(line_edit_value))
            self.setValue(line_edit_value)
        else:
            self.line_edit.setText(str(self.minimum))
            line_edit_value = self._getLineEditValue()
            self.slider.setValue(self._scaleLineEditToSlider(line_edit_value))
            self.setValue(line_edit_value)

    def _updateLineEdit(self):
        '''Updates the QLineEdit to reflect the current value of the QSlider.
        The method sets the value of the QLineEdit to the scaled value of the QSlider.
        '''
        slider_value = self._getSliderValue()
        self.line_edit.setText(str(self._scaleSliderToLineEdit(slider_value)))

    def _scaleLineEditToSlider(self, value):
        '''Converts a QLineEdit value to a scaled QSlider value. The method calculates
        the appropriate scale factor for the conversion using the minimum and maximum
        values of the QSlider and QLineEdit.
        Returns the scaled value.

        Parameters
        ----------
        value : float
        '''
        scale_factor = (self.slider_maximum - self.slider_minimum) / (self.maximum - self.minimum)
        value = self.slider_minimum + (scale_factor * (value - self.minimum))
        return int(value)

    def _scaleSliderToLineEdit(self, value):
        '''Converts a QSlider value to a scaled QLineEdit value. The method calculates
        the appropriate scale factor for the conversion using the minimum and maximum
        values of the QSlider and QLineEdit.
        Returns the scaled value, rounded as per the decimals property.

        Parameters
        ----------
        value : integer
        '''
        scale_factor = (self.maximum - self.minimum) / (self.slider_maximum - self.slider_minimum)
        value = self.minimum + (scale_factor * (value - self.slider_minimum))
        return round(float(value), self.decimals)
