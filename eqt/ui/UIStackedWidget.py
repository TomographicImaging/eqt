from eqt.ui.UIFormWidget import UIFormFactory
from PySide2 import QtWidgets
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QHBoxLayout, QVBoxLayout, QListWidget, QStackedWidget, QWidget


class UIStackedWidget(object):
    '''
    By default:

             QWidget or QDockWidget
    +----------------------------------------------------------+
    |        QVBoxLayout                                       |
    |   +---------------------------------------------------+  |
    |   |                                                   |  |
    |   |    +-------------------------------------------+  |  |
    |   |    |   QList                                   |  |  |
    |   |    |                                           |  |  |
    |   |    |                                           |  |  |
    |   |    +-------------------------------------------+  |  |
    |   |    +-------------------------------------------+  |  |
    |   |    |   QStackedWidget                          |  |  |
    |   |    |                                           |  |  |
    |   |    |                                           |  |  |
    |   |    +-------------------------------------------+  |  |
    |   |                                                   |  |
    |   +---------------------------------------------------+  |
    |                                                          |
    +----------------------------------------------------------+

    or if layout = horizontal:

             QWidget or QDockWidget
    +----------------------------------------------------------+
    |        QHBoxLayout                                       |
    |   +---------------------------------------------------+  |
    |   |                                                   |  |
    |   |    +--------------+   +------------------------+  |  |
    |   |    |   QList      |   |  QStackedWidget        |  |  |
    |   |    |              |   |                        |  |  |
    |   |    |              |   |                        |  |  |
    |   |    +--------------+   +------------------------+  |  |
    |   |                                                   |  |
    |   +---------------------------------------------------+  |
    |                                                          |
    +----------------------------------------------------------+


    '''

    def createStack(self, layout='vertical'):
        self.stack_list = QListWidget()
        self.list_margin_size = 11

        self.Stack = QStackedWidget(self)
        self.layout_type = layout

        if self.layout_type == 'horizontal':
            box = QHBoxLayout(self)
            self.list_margin_size = 18
            self.stack_list.setStyleSheet(
                "margin-top: {size}px"
                .format(size=self.list_margin_size))
        else:
            box = QVBoxLayout(self)
            self.stack_list.setStyleSheet(
                "margin-left : {size}px; margin-right : {size2}px"
                .format(size=self.list_margin_size,
                        size2=self.list_margin_size+1))

        box.addWidget(self.stack_list)
        box.addWidget(self.Stack)
        box.setAlignment(self.stack_list, Qt.AlignTop)

        self.setLayout(box)
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
        if self.layout_type != 'vertical':
            height_multiplier += 1
            self.stack_list.setMaximumWidth(
                self.stack_list.sizeHintForColumn(0)*1.2
                + self.list_margin_size*2)
            self.stack_list.setMaximumHeight(
                self.stack_list.sizeHintForRow(0)*height_multiplier
                + self.list_margin_size*2)
        self.stack_list.setMaximumHeight(
            self.stack_list.sizeHintForRow(0)*height_multiplier)

    def addTabs(self, titles):
        for title in titles:
            self.addTab(title=title)


class StackedWidget(QWidget, UIStackedWidget):
    def __init__(self, parent=None, layout='vertical'):
        # dockWidgetContents = QtWidgets.QWidget()

        QtWidgets.QWidget.__init__(self, parent)
        self.createStack(layout)


class StackedDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None, title=None, layout='vertical'):

        QtWidgets.QDockWidget.__init__(self, parent)
        widget = StackedWidget(parent, layout)
        self.setWidget(widget)
        if title is not None:
            self.setObjectName(title)
            self.setWindowTitle(title)

    def addTab(self, title, widget='form'):
        self.widget().addTab(title, widget)

    def addTabs(self, titles):
        self.widget().addTabs(titles)


class StackedWidgetFactory(QWidget):
    '''creates a StackedWidget with a list of the widgets' titles
    to the left hand side.
    The returned dockWidget must be added with
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    '''

    def getQDockWidget(parent=None, title=None, layout='vertical'):
        return StackedDockWidget(parent, title, layout)

    def getQWidget(parent=None, layout='vertical'):
        return StackedWidget(parent, layout)
