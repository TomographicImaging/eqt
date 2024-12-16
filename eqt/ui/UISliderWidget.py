from PySide2 import QtCore
from PySide2.QtWidgets import QSlider


class UISliderWidget(QSlider):
    '''Creates a Slider widget which updates
    a QLabel with its value (which may be scaled
    to a non-integer value by setting the scale_factor)'''
    def __init__(self, dspinbox, min=0.00, max=1.00, scale_factor=1, parent=None):
        QSlider.__init__(self)
        self.parent = parent
        self.scale_factor = scale_factor

        self.setOrientation(QtCore.Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setTickPosition(QSlider.TicksBelow)

        self.sliderPressed.connect(self.update_dspinbox)
        self.sliderMoved.connect(self.update_dspinbox)
        self.sliderReleased.connect(self.update_dspinbox)

        self.dspinbox = dspinbox
        self.dspinbox.editingFinished.connect(self.update_slider)

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
