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

    def addTab(self, label, widget='form', title=None, number_title=True):
        ''' Adds a tab to the StackedWidget.
        
        Parameters
        ----------
        label: str
            The name that will be used to refer to the tab.
        title: str
            The name the tab will be listed as in the QListWidget.
        number_title: bool, default True
            Determines whether the title of the tab is generated 
            by adding a number in front of the label. E.g. if the
            label is "FBP" and this is the first tab that has been
            added then the title will be "1 - FBP" if number_title
            has been set to True and title=None
        widget: QWidget or str: 'form', default 'form'
            the widget that will be contained in the tab.
            by default this is set to 'form' which means an empty
            FormWidget is created'''

        if title is None:
            if number_title:
                title_num = len(self.tabs) + 1
                title = "{} - {}".format(str(title_num), label)
            else:
                raise Exception('''The title of the tab has not been set.
                    Please set title - this must be a string, or set number_title to True.''')
        self.stack_list.addItem(title)

        if widget == 'form':
            widget = UIFormFactory.getQWidget(self)

        self.Stack.addWidget(widget)
        self.tabs[label] = widget
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

    def addTabs(self, labels):
        '''
        Adds multiple tabs to the StackedWidget
        All tabs contain an empty FormWidget and their title is
        their label, plus they are numbered according to their order.
        Parameters
        ----------
        labels: list of str
            The names that will be used to refer to the tabs.
        '''
        for label in labels:
            self.addTab(label)

    def getTab(self, label):
        ''' return the tab with label: label
        Parameter
        ---------
        label: str
            The label of the tab to be returned.
            Note, the label may be different to the tab's title.'''
        return self.tabs[label]

    def getTabs(self):
        ''' return the dict of tabs'''
        return self.tabs



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

    def getTab(self, label):
        return self.widget().getTab(label)

    def getTabs(self):
        return self.widget().getTabs()


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
