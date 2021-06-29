from eqt.ui.UIFormWidget import UIFormFactory
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QListWidget, QStackedWidget, QWidget


class UIStackedWidget(object):

    def createStack(self):
        self.stack_list = QListWidget()
        self.margin_size = 20
        self.stack_list.setStyleSheet("margin : {}px".format(self.margin_size))

        self.Stack = QStackedWidget(self)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.stack_list)
        hbox.addWidget(self.Stack)
        hbox.setAlignment(self.stack_list, Qt.AlignTop)

        self.setLayout(hbox)
        self.stack_list.currentRowChanged.connect(self.display)

        self.tabs = {}

        self.num_tabs = 0
        self.widgets = {}

    def display(self, i):
        self.Stack.setCurrentIndex(i)

    def currentIndex(self):
        return self.Stack.currentIndex()

    def addTab(self, title, widget='form'):
        self.stack_list.addItem(title)

        if widget == 'form':
            widget = UIFormFactory.getQWidget(self)

        self.Stack.addWidget(widget)
        self.tabs[title] = widget
        self.num_tabs += 1
        height_multiplier = self.num_tabs + 1
        self.stack_list.setMaximumWidth(
            self.stack_list.sizeHintForColumn(0)*1.2 + self.margin_size*2)
        self.stack_list.setMaximumHeight(
            self.stack_list.sizeHintForRow(0)*height_multiplier
            + self.margin_size*2)

    def addTabs(self, titles):
        for title in titles:
            self.addTab(title=title)


class StackedWidget(QWidget, UIStackedWidget):
    def __init__(self, parent=None):
        # dockWidgetContents = QtWidgets.QWidget()

        QtWidgets.QWidget.__init__(self, parent)
        self.createStack()


class StackedDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None, title=None):

        QtWidgets.QDockWidget.__init__(self, parent)
        widget = StackedWidget(parent)
        self.setWidget(widget)
        if title is not None:
            self.setObjectName(title)
            self.setWindowTitle(title)

    def addTab(self, title, widget='form'):
        self.widget().addTab(title, widget)

    def addTabs(self, titles):
        self.widget().addTabs(titles)


class StackedWidgetFactory(QWidget):

    def getQDockWidget(parent=None, title=None):
        return StackedDockWidget(parent)

    def getQWidget(parent=None):
        return StackedWidget(parent)
