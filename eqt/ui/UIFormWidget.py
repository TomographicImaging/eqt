from PySide2 import QtCore, QtWidgets, QtGui
# from PyQt5.QtWidgets import QProgressDialog, QDialog, QLabel, QComboBox, QDialogButtonBox, QFormLayout, QWidget, QVBoxLayout, \
#     QGroupBox, QLineEdit, QMessageBox, QPushButton


        

class UIFormWidget(object):
    '''
             QWidget or QDockWidget
    +----------------------------------------------------------+
    |        QVBoxLayout                                       |
    |   +---------------------------------------------------+  |
    |   |    QGroupBox                                      |  |
    |   |                                                   |  |
    |   |    +------------------------------------------+   |  |
    |   |    |   QFormLayout                            |   |  |
    |   |    |                                          |   |  |
    |   |    |                                          |   |  |
    |   |    +------------------------------------------+   |  |
    |   |                                                   |  |
    |   +---------------------------------------------------+  |
    |                                                          |
    +----------------------------------------------------------+
    '''
    def createForm(self):
        # Add vertical layout to dock contents
        verticalLayout = QtWidgets.QVBoxLayout(self)
        verticalLayout.setContentsMargins(10, 10, 10, 10)

        # Add vertical layout to main widget (self)
        # verticalLayout.addWidget(self)
        self.setLayout(verticalLayout)
        
        # Add group box
        groupBox = QtWidgets.QGroupBox(self)

        # Add form layout to group box
        groupBoxFormLayout = QtWidgets.QFormLayout(groupBox)

        # Add elements to layout
        verticalLayout.addWidget(groupBox)

        self.num_widgets = 0
        self.uiElements = {
                'verticalLayout':verticalLayout, 
                'groupBox' : groupBox,
                'groupBoxFormLayout': groupBoxFormLayout}
        self.widgets = {}

    @property
    def groupBox(self):
        return self.uiElements['groupBox']
                
    def addWidget(self, qwidget, qlabel, name):

        formLayout = self.uiElements['groupBoxFormLayout']
                
        #Create the widgets:

        widgetno = self.num_widgets

        # add the label
        label = '{}_label'.format(name)
        if isinstance (qlabel, str):
            txt = qlabel
            qlabel = QtWidgets.QLabel(self.uiElements['groupBox'])
            qlabel.setText(txt)
        formLayout.setWidget(widgetno, QtWidgets.QFormLayout.LabelRole, qlabel)

        # add the field
        field = '{}_field'.format(name)
        formLayout.setWidget(widgetno, QtWidgets.QFormLayout.FieldRole, qwidget)

        # save a reference to the widgets in the dictionary
        self.widgets[label] = qlabel
        self.widgets[field] = qwidget
        self.num_widgets += 1



class FormWidget(QtWidgets.QWidget, UIFormWidget):
    def __init__(self, parent=None):
    # dockWidgetContents = QtWidgets.QWidget()
        
        QtWidgets.QWidget.__init__(self, parent)
        self.createForm()

class FormDockWidget(QtWidgets.QDockWidget, UIFormWidget):
    def __init__(self, parent=None, title=None):
    # dockWidgetContents = QtWidgets.QWidget()
        
        QtWidgets.QDockWidget.__init__(self, parent)
        self.createForm()
        if title is not None:
            self.setObjectName(title)

class UIFormFactory(QtWidgets.QWidget):
# def generateUIFormView(QtWidgets.QWidget):
    '''creates a widget with a form layout group to add things to

    basically you can add widget to the returned groupBoxFormLayout and paramsGroupBox
    The returned dockWidget must be added with
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    '''
    @staticmethod
    def getQDockWidget(parent=None):
        return FormDockWidget(parent)
    @staticmethod
    def getQWidget(parent=None):
        return FormWidget(parent)