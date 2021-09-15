from PySide2 import QtCore
from PySide2.QtWidgets import QSlider

class UISliderWidget(QSlider):
    '''Creates a Slider widget which updates
    a QLabel with its value (which may be scaled
    to a non-integer value by setting the scale_factor)'''
    def __init__(self, label, scale_factor=1):
        QSlider.__init__(self)
        self.label = label
        self.scale_factor = scale_factor
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setFocusPolicy(QtCore.Qt.StrongFocus) 
        self.setTickPosition(QSlider.TicksBelow) 
        self.valueChanged.connect(self.show_slider_value)

    def get_slider_value(self):
       return self.value()*self.scale_factor

    def show_slider_value(self):
        value = self.get_slider_value()
        self.label.setText(str(value))