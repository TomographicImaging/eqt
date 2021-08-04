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
        '''
        Adds a widget to the layout.
        layout = 'form' - adds to the FormLayout
        layout = 'vertical' - adds to the Vertical layout below the form.
        To add to the form layout, qlabel and name must be passed.
        '''
        
        if layout == 'vertical':
            if [name, qlabel] != [None, None]:
                raise ValueError('qlabel {} and name {} have been passed but would be discarded with layout=vertical. If this is unexpected, have a look at your code.') 
            self.formWidget.uiElements['verticalLayout'].addWidget(qwidget)
        elif layout == 'form':
            if name is None:
                raise ValueError('To add the widget to the form, please set name.')
            if qlabel is None:
                raise ValueError('To add the widget to the form, please set label.')
            self.formWidget.addWidget(qwidget, qlabel, name)
        else:
           raise ValueError("layout {} is not recognised, must be set to 'form' or 'vertical'.".format(layout))  

    def addSpanningWidget(self, qwidget, name=None, layout='form'):
        '''
        Adds a spanning widget to the layout.
        layout = 'form' - adds the widget to the FormLayout
        layout = 'vertical' - adds the widget to the Vertical layout below the form.
        To add to the form layout, name must be passed.
        '''
        if layout == 'vertical':
            if name is not None:
                raise ValueError('name {} has been passed but would be discarded with layout=vertical. If this is unexpected, have a look at your code.') 
            self.formWidget.uiElements['verticalLayout'].addWidget(qwidget)
        elif layout == 'form':
            if name is None:
                raise ValueError('To add the widget to the form, please set name.')
            self.formWidget.addSpanningWidget(qwidget, name)
        else:
            raise ValueError("layout {} is not recognised, must be set to 'form' or 'vertical'.".format(layout))
    
    def insertWidget(self, index, qwidget):
        '''inserts a widget to the vertical layout at the specific index'''
        self.formWidget.uiElements['verticalLayout'].insertWidget(index, qwidget)
        