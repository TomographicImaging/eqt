from PySide2 import QtCore
from PySide2.QtWidgets import QDoubleSpinBox, QGridLayout, QLabel, QSlider, QWidget


class UISliderLineEditWidget(QWidget):
    '''Creates a QGridLayout that includes a QSlider, min/max QLabels and a QDoubleSpinBox.
    The QDoubleSpinBox is updated with the value of the slider and vice versa.

    Parameters
    ----------
    dspinbox : QDoubleSpinBox
    min : float
    max : float
    step_size : float
    '''
    def __init__(self, minimum=0.00, maximum=1.00, step_size=1.00):
        QWidget.__init__(self)

        # Configure the QSlider
        self.slider = QSlider()
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setSingleStep(step_size)
        self.slider.setTickInterval(step_size)

        # Connect the QSlider to the QDoubleSpinBox
        self.slider.sliderPressed.connect(self.update_dspinbox)
        self.slider.sliderMoved.connect(self.update_dspinbox)
        self.slider.sliderReleased.connect(self.update_dspinbox)

        # Connect the QDoubleSpinBox
        self.dspinbox = QDoubleSpinBox()
        self.dspinbox.valueChanged.connect(self.update_slider)
        self.dspinbox.setMinimum(minimum)
        self.dspinbox.setMaximum(maximum)

        # Configure the min/max QLabels
        self.min_label = QLabel()
        self.min_label.setText(str(self.slider.minimum()))
        self.max_label = QLabel()
        self.max_label.setText(str(self.slider.maximum()))

        # Configure the QGridLayout
        widget_layout = QGridLayout()
        widget_layout.addWidget(self.slider, 0, 0, 1, -1)
        widget_layout.addWidget(self.min_label, 1, 0, QtCore.Qt.AlignLeft)
        widget_layout.addWidget(self.max_label, 1, 1, QtCore.Qt.AlignRight)
        widget_layout.addWidget(self.dspinbox, 2, 0, 1, -1)

        # Set the layout
        self.setLayout(widget_layout)
        self.show()

    def get_slider_value(self):
        return self.slider.value()

    def get_dspinbox_value(self):
        return self.dspinbox.value()

    def update_slider(self):
        dspinbox_value = int(self.get_dspinbox_value())
        self.slider.setValue(dspinbox_value)

    def update_dspinbox(self):
        slider_value = float(self.get_slider_value())
        self.dspinbox.setValue(slider_value)
