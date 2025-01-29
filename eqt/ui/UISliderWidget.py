from qtpy import QtCore, QtGui
from qtpy.QtWidgets import QApplication, QGridLayout, QLabel, QLineEdit, QSlider, QWidget


class UISliderWidget(QWidget):
    '''Creates a QSlider widget with an attached QLineEdit, displaying minimum, maximum
    and median values.

    This class creates a QGridLayout that includes a QSlider, min/median/max QLabels and
    a QLineEdit. The QSlider value changes with the QLineEdit value and vice versa.

    The value() and setValue() methods provide an interface for external widgets to
    get and set the value of the widget. Some private methods exist (e.g. _setDecimals())
    that are responsible for validating and setting arguments.
    '''
    def __init__(self, minimum, maximum, decimals=2, number_of_steps=2000, number_of_ticks=10):
        '''Creates the QGridLayout and the widgets that populate it (QSlider, QLineEdit,
        QLabels). Also sets some attributes.

        The arrangement of the widgets is configured.

        Signals from the QSlider and QLineEdit are connected, linking user interactions
        with these widgets. The update methods call the scaling methods so that value
        changes are accurately represented in the other.

        Parameters
        ----------
        minimum : float
            - Minimum value of the QLineEdit, must be less than the maximum.
        maximum : float
            - Maximum value of the QLineEdit, must be greater than the minimum.
        decimals : int
            - Number of decimal places that the QLabels, QLineEdit and QSlider steps can display
        number_of_steps : int
            - Number of steps in the QSlider
        number_of_ticks : int
            - Number of ticks visualised under the QSlider, determines tick interval
        '''
        QWidget.__init__(self)

        self._setDecimals(decimals)
        self._setMinimumMaximum(minimum, maximum)
        self.median = round((self.maximum - self.minimum) / 2 + self.minimum, self.decimals)

        self._setNumberOfSteps(number_of_steps)
        self._setNumberOfTicks(number_of_ticks)

        self.slider_minimum = 0
        self.slider_maximum = self.number_of_steps
        self.scale_factor = (self.slider_maximum - self.slider_minimum) / (self.maximum -
                                                                           self.minimum)

        self.step_size = float((self.maximum - self.minimum) / self.number_of_steps)
        self.tick_interval = round(
            (self.slider_maximum - self.slider_minimum) / self.number_of_ticks)

        self._setUpQSlider()
        self._setUpQValidator()
        self._setUpQLineEdit()
        self._connectFocusChangedSignal()
        self._setUpQLabels()
        self._setUpQGridLayout()

        self.setLayout(self.widget_layout)

    def value(self):
        '''Defines the value of the UISliderWidget using the current float value of the QLineEdit.
        This method exists to remain consistent with other QWidgets.
        '''
        return float(self._getQLineEditValue())

    def setValue(self, value):
        '''Sets the value of the UISliderWidget using the current float value of the QLineEdit.
        To avoid the updated QSlider overwriting the QLineEdit value, QSlider is
        updated first with the scaled value.
        This method exists to remain consistent with other QWidgets.

        Parameters
        ----------
        value : float
        '''
        self.slider.setValue(self._scaleLineEditToSlider(value))
        self.line_edit.setText(str(value))

    def _setMinimumMaximum(self, minimum, maximum):
        '''Sets the widget's minimum and maximum attributes. Checks that the minimum
        '''
        if minimum >= maximum:
            raise ValueError("'minimum' argument must be less than 'maximum'")
        else:
            self.minimum = round(minimum, self.decimals)
            self.maximum = round(maximum, self.decimals)

    def _setDecimals(self, decimals):
        '''Sets the number of decimal places that the QLabels, QLineEdit and
        QSlider steps can display. Checks that the argument provided is valid,
        i.e. that it is a positive integer value - an invalid value raises
        a ValueError during object instantiation.

        Parameters
        ----------
        decimals : int
        '''
        if decimals <= 0:
            raise ValueError("'decimals' value must be greater than 0")
        elif isinstance(decimals, int) is not True:
            raise TypeError("'decimals' value type must be int")
        else:
            self.decimals = decimals

    def _setNumberOfSteps(self, number_of_steps):
        '''Sets the number of steps in the QSlider. Steps are each subdivision of the
        QSlider's range. Also checks that the argument provided is valid, i.e. that
        it is a positive integer value - an invalid value raises
        a ValueError during object instantiation.

        Parameters
        ----------
        number_of_steps : int
        '''
        if number_of_steps <= 0:
            raise ValueError("'number_of_steps' value must be greater than 0")
        elif isinstance(number_of_steps, int) is not True:
            raise TypeError("'number_of_steps' value type must be int")
        else:
            self.number_of_steps = number_of_steps

    def _setNumberOfTicks(self, number_of_ticks):
        '''Sets the number of ticks that the QSlider displays. Ticks are the notches
        displayed underneath the QSlider. Also checks that the argument provided is
        valid, i.e. that it is a positive integer value - an invalid value raises
        a ValueError during object instantiation.

        Parameters
        ----------
        number_of_ticks : int
        '''
        if number_of_ticks <= 0:
            raise ValueError("'number_of_ticks' value must be greater than 0")
        elif isinstance(number_of_ticks, int) is not True:
            raise TypeError("'number_of_ticks' value type must be int")
        else:
            self.number_of_ticks = number_of_ticks

    def _setUpQSlider(self):
        '''Creates and configures the UISlider's QSlider widget.
        A signal from the QSlider is connected to the method that
        updates the QLineEdit widget.
        '''
        self.slider = QSlider()
        self.slider.setRange(self.slider_minimum, self.slider_maximum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setTickInterval(self.tick_interval)

        self.slider.valueChanged.connect(self._updateQLineEdit)

    def _setUpQValidator(self):
        '''Creates and configures the UISlider's QValidator widget.
        The QValidator validates user input from the QLineEdit.
        The locale is set to "en_US" to enforce the correct
        decimal format (i.e. '3.14', instead of '3,14').
        '''
        self.validator = QtGui.QDoubleValidator()
        self.validator.setBottom(self.minimum)
        self.validator.setTop(self.maximum)
        self.validator.setNotation(QtGui.QDoubleValidator.StandardNotation)
        self.validator.setLocale(QtCore.QLocale("en_US"))

    def _setUpQLineEdit(self):
        '''Creates and configures the UISlider's QLineEdit widget.
        Signals from the QLineEdit are connected to the method that
        updates the QSlider widget.
        '''
        self.line_edit = QLineEdit()
        self.line_edit.setValidator(self.validator)
        self.line_edit.setText(str(self.minimum))
        self.line_edit.setClearButtonEnabled(True)
        self.line_edit.setPlaceholderText(str(self.minimum))

        self.line_edit.editingFinished.connect(self._updateQSlider)
        self.line_edit.returnPressed.connect(self._updateQSlider)

    def _connectFocusChangedSignal(self):
        '''References the existing QApplication instance to connect
        its focusChanged signal to the method that updates the
        QSlider. If the focus changes, i.e. the QLineEdit loses focus,
        the QSlider will be updated.
        '''
        self.app = QApplication.instance()
        self.app.focusChanged.connect(self._updateQSlider)

    def _setUpQLabels(self):
        '''Creates and configures the UISlider's QLabel widgets.
        The QLabels display the minimum, median and maximum values underneath
        the QSlider.
        '''
        self.min_label = QLabel()
        self.min_label.setText(str(self.minimum))
        self.median_label = QLabel()
        self.median_label.setText(str(self.median))
        self.max_label = QLabel()
        self.max_label.setText(str(self.maximum))

    def _setUpQGridLayout(self):
        '''Creates a QGridLayout. Also adds the UISlider's widgets to the QGridLayout.
        The QSlider is added to the first row of the QGridLayout and spans the entire row.
        The QLabels are added to the second row and are aligned to the left, right and center
        of the QSlider.
        The QLineEdit is added to the third row and also spans the entire row.
        '''
        self.widget_layout = QGridLayout()
        self.widget_layout.addWidget(self.slider, 0, 0, 1, -1)
        self.widget_layout.addWidget(self.min_label, 1, 0, QtCore.Qt.AlignLeft)
        self.widget_layout.addWidget(self.median_label, 1, 1, QtCore.Qt.AlignCenter)
        self.widget_layout.addWidget(self.max_label, 1, 2, QtCore.Qt.AlignRight)
        self.widget_layout.addWidget(self.line_edit, 2, 0, 1, -1)

    def _getQSliderValue(self):
        '''Gets the current value of the QSlider, returning either 0 or a positive integer.
        '''
        return self.slider.value()

    def _getQLineEditValue(self):
        '''Gets the current value of the QLineEdit. Returns a string value between the
        UISliderWidget's minimum and maximum values.
        '''
        return self.line_edit.text()

    def _updateQSlider(self):
        '''Updates the QSlider to reflect the current value of the QLineEdit.
        The method uses the state of the QValidator to check that the QLineEdit
        value is valid - if it is valid, it sets the value of the QSlider to the
        scaled value of the QLineEdit. Otherwise, it will update the QSlider with
        either the scaled value of the QLineEdit's minimum or maximum. Values
        outside the range will raise a ValueError.
        '''
        if self._getQLineEditValue() == '':
            self.line_edit.setText(str(self.minimum))

        line_edit_value = float(self._getQLineEditValue())
        state = self.validator.validate(self.line_edit.text(), 0)
        if state[0] == QtGui.QDoubleValidator.Acceptable:
            scaled_value = self._scaleLineEditToSlider(line_edit_value)
            self.slider.setValue(scaled_value)
            self.setValue(line_edit_value)
        elif line_edit_value > self.maximum:
            self.line_edit.setText(str(self.maximum))
            self.slider.setValue(self.slider_maximum)
            self.setValue(self.maximum)
            raise ValueError("range exceeded: resetting to 'maximum'")
        elif line_edit_value < self.minimum:
            self.line_edit.setText(str(self.minimum))
            self.slider.setValue(self.slider_minimum)
            self.setValue(self.minimum)
            raise ValueError("range exceeded: resetting to 'minimum'")

    def _updateQLineEdit(self):
        '''Updates the QLineEdit to reflect the current value of the QSlider.
        The method sets the value of the QLineEdit to the scaled value of the QSlider.
        '''
        slider_value = self._getQSliderValue()
        self.line_edit.setText(str(self._scaleSliderToLineEdit(slider_value)))

    def _scaleLineEditToSlider(self, value):
        '''Converts a QLineEdit value to a scaled QSlider value. The method calculates
        the scale factor for the conversion using the minimum and maximum
        values of the QSlider and QLineEdit.
        Returns the scaled value.

        Parameters
        ----------
        value : float
        '''
        value = self.slider_minimum + (self.scale_factor * (value - self.minimum))
        return int(value)

    def _scaleSliderToLineEdit(self, value):
        '''Converts a QSlider value to a scaled QLineEdit value. The method calculates
        the scale factor for the conversion using the minimum and maximum
        values of the QSlider and QLineEdit.
        Returns the scaled value, rounded as per the decimals property.

        Parameters
        ----------
        value : integer
        '''
        value = self.minimum + (1 / self.scale_factor * (value - self.slider_minimum))
        return round(float(value), self.decimals)
