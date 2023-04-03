# Author: Edoardo Pasca, Laura Murgatroyd

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

    def getWidget(self, name, role='field'):
        '''returns the Widget by the name with which it has been added
        
        By default it returns the widget that is the field in the form. 
        The user can get the label by specifying the role to be label
        
        Raises ValueError if the role is not field or label.
        '''
        return self.formWidget.getWidget(name, role)

    def getWidgets(self):
        '''returns a dictionary of all the widgets in the form'''
        return self.formWidget.getWidgets()
    
    def setWidgetVisible(self, name, visible):
        '''
        Sets the visibility of the widget and associated label with the given name.
        Parameters:
            visible: bool
                True to set the widget visible, False to hide it
            name: str
                The name of the widget to set visible/invisible
        '''

        self.formWidget.setWidgetVisible(name, visible)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets in the form.
        This can be used to restore the state of the widgets using the restoreAllSavedWidgetStates method.
        '''
        self.formWidget.saveAllWidgetStates()

    def restoreAllSavedWidgetStates(self):
        '''
        Restores the state of all widgets in the form to the state saved by the saveAllWidgetStates method.
        If the saveAllWidgetStates method has not been called, this method will do nothing.
        '''
        self.formWidget.restoreAllSavedWidgetStates()

    def getAllWidgetStates(self):
        '''
        Returns a dictionary of the state of all widgets in the form.
        Returns
        -------
        state: dict
            A dictionary of the state of the widget/s, with the key/s being the name of the widget/s, and the value/s
            being a dictionary with the keys 'value', 'enabled', and 'visible', which store the value, enabled state,
            and visible state of the widget. The value may be a string, boolean, or integer, depending on the type of widget.
            E.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True}, 'widget2': {'value': 2, 'enabled': False, 'visible': False}}
        '''
        return self.formWidget.getAllWidgetStates()

    def getWidgetState(self, widget, role=None):
        '''
        Returns the state of the widget.

        Parameters
        ----------
        widget: QWidget or str
            The widget to get the state of, or the name of the widget to get the state of, in which case it will be retrieved from
            the widgets dictionary using the name.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to get the state of. This is only used if widget is a string.
            If not given, the state will be returned for the widget with name: widget.
            If this fails, and the role is not given, the state will be returned for the widget with name: widget_field.
            If given, the state will be returned for the widget with name: widget_role.

        
        Returns
        -------
        dict
            A dictionary of the state of the widget, with the keys 'value', 'enabled', and 'visible',
            which store the value, enabled state, and visible state of the widget.
            The value may be a string, boolean, or integer, depending on the type of widget.
            E.g. {'value': 1, 'enabled': True, 'visible': True}
            This dictionary can be used to restore the state of the widget using the setWidgetState method.
        '''
        return self.formWidget.getWidgetState(widget, role)

    def applyWidgetState(self, name, state, role=None):
        '''
        Applies the given state to the widget with the given name.

        Parameters
        ----------
        name: str
            The name of the widget to apply the state to
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to. If not given, the state will be applied to the widget with name: name.
            If this fails, and the role is not given, the state will be applied to the widget with name: name_field.
            If given, the state will be applied to the widget with name: name_role.
        state: dict
            A dictionary of the state of the widget, with  keys 'value', 'enabled', and 'visible', which store the value, enabled state,
            and visible state of the widget.
            The value may be a string, boolean, or integer, depending on the type of widget.
            E.g. {'value': 1, 'enabled': True, 'visible': True}
        '''
        return self.formWidget.applyWidgetState(name, state, role)

    def applyWidgetStates(self, state):
        '''
        Applies the given state to the widgets in the form given by the keys of the state dictionary.

        Parameters
        ----------
        state: dict
            A dictionary of the state of the widgets, with the keys being the name of the widgets, and the value
            being a dictionary with the keys 'value', 'enabled', and 'visible', which store the value, enabled state,
            and visible state of the widget.
            The value may be a string, boolean, or integer, depending on the type of widget.
            E.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True}, 'widget2': {'value': 2, 'enabled': False, 'visible': False}}
        '''
        return self.formWidget.applyWidgetStates(state)
        