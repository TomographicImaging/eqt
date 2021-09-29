from PySide2 import QtWidgets
from PySide2.QtWidgets import (QPushButton, QFrame, QHBoxLayout, QGroupBox)
from PySide2.QtCore import Qt


class UIMultiStepWidget(object):
    '''
             QWidget or QDockWidget
    +----------------------------------------------------------+
    |        QVBoxLayout                                       |
    |                                                          |
    |                                                          |
    |                                                          |
    |                                                          |
    |                                                          |
    |                                                          |
    |       _______________               _____________        |
    |      | Previous Step |             | Next Step   |       |
    +----------------------------------------------------------+
    '''

    def createWidget(self):
        # Add vertical layout to dock contents
        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setContentsMargins(10, 10, 10, 10)
        verticalLayout.setAlignment(Qt.AlignTop)

        # Add vertical layout to main widget (self)
        self.setLayout(verticalLayout)

        # Add the next and previous buttons:
        horizontalGroupBox = QGroupBox()
        horizontalGroupBox.setContentsMargins(0,0,0,0)
        horizontalLayout = QHBoxLayout()
        horizontalGroupBox.setLayout(horizontalLayout)
        horizontalGroupBox.setFlat(True)
        verticalLayout.addWidget(horizontalGroupBox)

        next_button = QPushButton("Next step")
        prev_button = QPushButton("Previous step")
        prev_button.setEnabled(False)
        prev_button.clicked.connect(lambda: self.updateStep('prev'))
        next_button.clicked.connect(lambda: self.updateStep('next'))
        horizontalLayout.addWidget(prev_button)
        horizontalLayout.addWidget(next_button)
        self.next_button = next_button
        self.prev_button = prev_button

        self.current_step = -1

        self.uiElements = {
            'verticalLayout': verticalLayout,
            'buttonGroupBox': horizontalGroupBox,
            }
        self.widgets = {}

    def updateStep(self, go_to="next"):
        steps = list(self.widgets.keys())
        step_widgets = list(self.widgets.values())
        current_step_index = steps.index(self.current_step)

        if go_to == 'next':
            self.prev_button.setEnabled(True)
            next_index = current_step_index + 1
            if next_index == len(steps)-1:
                self.next_button.setEnabled(False)
            else:
                self.next_button.setEnabled(True)
            
        if go_to == 'prev':
            self.next_button.setEnabled(True)
            next_index = current_step_index - 1
            if next_index == 0:
                self.prev_button.setEnabled(False)
            else:
                self.prev_button.setEnabled(True)

        self.current_step = steps[next_index]

        widgets_to_show = step_widgets.pop(next_index)
        widgets_to_hide = step_widgets
        self.showHideWidgets(widgets_to_hide, show=False)
        self.showHideWidgets(widgets_to_show, show=True)

    def addStepWidget(self, qwidget, name):
        if self.current_step == -1:
            self.current_step = name
        else:
            self.showHideWidgets(qwidget, show=False)
        self.widgets[name] = qwidget
        # insert widget above next and previous buttons
        self.uiElements['verticalLayout'].insertWidget(0, qwidget)

    def addStepWidgets(self, qwidgets, name):
        for qwidget in qwidgets:
            self.addStepWidget(qwidget, name)

    def showHideWidgets(self, widgets, show=True):
        if type(widgets) != list:
            widgets = [widgets]
        for widget in widgets:
            widget.setVisible(show)


class MultiStepWidget(QtWidgets.QWidget, UIMultiStepWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.createWidget()


class MultiStepDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None, title=None):
        QtWidgets.QDockWidget.__init__(self, parent)
        widget = MultiStepWidget(parent)
        self.setWidget(widget)
        if title is not None:
            self.setObjectName(title)

    def addWidget(self, qwidget, qlabel, name):
        self.widget().addWidget(qwidget, qlabel, name)

    def addStepWidget(self, qwidget, name):
        self.widget().addStepWidget(qwidget, name)

    def addStepWidgets(self, qwidgets, name):
        self.widget().addStepWidgets(qwidgets, name)


class UIMultiStepFactory(QtWidgets.QWidget):
    '''creates a widget with a vertical layout, with "next" and "previous"
    buttons at the bottom of the layout.

    you can add a widget to the vertical layout, using addStepWidget.
    The first step added will be shown to begin with, and the other steps 
    can be navigated between, using the next and previous buttons.

    The returned dockWidget must be added with
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    '''
    @staticmethod
    def getQDockWidget(parent=None):
        return MultiStepDockWidget(parent)

    @staticmethod
    def getQWidget(parent=None):
        return MultiStepWidget(parent)
