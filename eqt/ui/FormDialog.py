from PySide2 import QtCore, QtGui, QtWidgets
from eqt.ui import UIFormFactory

class FormDialog(QtWidgets.QDialog):
    def __init__(self, parent = None, title=None):
        
        QtWidgets.QDialog.__init__(self, parent)
        
        # button box
        bb = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                                     | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox = bb

        formWidget = UIFormFactory.getQWidget(parent=self)
        self.formWidget = formWidget

        # set the layout of the dialog
        self.setLayout(formWidget.uiElements['verticalLayout'])
        
        if title is not None:
            self.setWindowTitle(title)
        # add button box to the UI
        self.formWidget.uiElements['verticalLayout'].addWidget(bb)

    @property
    def Ok(self):
        '''returns a reference to the Dialog Ok button to connect its signals'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)
    @property
    def Cancel(self):
        '''returns a reference to the Dialog Cancel button to connect its signals'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)

    @property
    def widgets(self):
        return self.formWidget.widgets
    @property
    def groupBox(self):
        return self.formWidget.groupBox

    def addWidget(self, qwidget, qlabel=None, name=None, layout='form'):
        '''adds a widget to the layout

        if qlabel and name are passed they will be populating the FormLayout,
        otherwise they will be added in the vertical layout below the FormLayout
        '''
        
        if layout == 'vertical':
            if [name, qlabel] != [None, None]:
                raise ValueError('qlabel {} and name {} have been passed but would be discarded with layout=vertical. If this is unexpected, have a look at your code.') 
            self.formWidget.uiElements['verticalLayout'].addWidget(qwidget)
        elif name is None:
            raise ValueError('To add the widget to the form, please set name.')
        else:
            self.formWidget.addWidget(qwidget, qlabel, name)
    
    def insertWidget(self, index, qwidget):
        '''inserts a widget to the FormLayout vertical layout at the specific index'''
        self.formWidget.uiElements['verticalLayout'].insertWidget(index, qwidget)
        