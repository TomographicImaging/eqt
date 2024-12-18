from PySide2 import QtCore
from PySide2.QtWidgets import QSlider


class UISliderWidget(QSlider):
    '''Creates a Slider widget which updates
    a QDoubleSpinBox with its value (which may be scaled
    to a non-integer value by setting the scale_factor)

    Parameters
    ----------
    dspinbox : QDoubleSpinBox
    min : float
    max : float
    step_size : float
    '''
    def __init__(self, dspinbox, minimum=0.00, maximum=1.00, step_size=1.00):
        QSlider.__init__(self)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.steps = (maximum-minimum) / step_size

        self.setOrientation(QtCore.Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setTickPosition(QSlider.TicksBelow)
        self.setSingleStep(step_size)
        self.setTickInterval(step_size)

        self.sliderPressed.connect(self.update_dspinbox)
        self.sliderMoved.connect(self.update_dspinbox)
        self.sliderReleased.connect(self.update_dspinbox)

        self.dspinbox = dspinbox
        self.dspinbox.valueChanged.connect(self.update_slider)
        self.dspinbox.setMinimum(minimum)
        self.dspinbox.setMaximum(maximum)

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

    def setMaximum(self, arg__1):
        return super().setMaximum(arg__1)
