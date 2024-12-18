from PySide2 import QtCore
from PySide2.QtWidgets import QSlider


class UISliderWidget(QSlider):
    '''Creates a Slider widget which updates
    a QDoubleSpinBox with its value (which may be scaled
    to a non-integer value by setting the scale_factor)

    Parameters
    ----------
    dspinbox : QDoubleSpinBox
    min_label : QLabel
    max_label : QLabel
    min : float
    max : float
    step_size : float
    '''
    def __init__(self, dspinbox, min_label, max_label, minimum=0.00, maximum=1.00, step_size=1.00):
        QSlider.__init__(self)

        # Configure the QSlider
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setTickPosition(QSlider.TicksBelow)
        self.setSingleStep(step_size)
        self.setTickInterval(step_size)

        # Connect the QSlider to the QDoubleSpinBox
        self.sliderPressed.connect(self.update_dspinbox)
        self.sliderMoved.connect(self.update_dspinbox)
        self.sliderReleased.connect(self.update_dspinbox)

        # Configure the QDoubleSpinBox
        self.dspinbox = dspinbox
        self.dspinbox.setDecimals(3)
        self.dspinbox.setMinimum(minimum)
        self.dspinbox.setMaximum(maximum)

        # Connect the QDoubleSpinBox to the QSlider
        self.dspinbox.valueChanged.connect(self.update_slider)

        # Configure QLabels for minimum and maximum QSlider values
        self.min_label = min_label
        self.max_label = max_label

    def get_slider_value(self):
        return self.value()

    def get_dspinbox_value(self):
        return self.dspinbox.value()

    def update_slider(self):
        dspinbox_value = int(self.get_dspinbox_value())
        self.setValue(dspinbox_value)

    def update_dspinbox(self):
        slider_value = float(self.get_slider_value())
        self.dspinbox.setValue(slider_value)
