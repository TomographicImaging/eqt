from PySide2 import QtWidgets

from . import UIFormFactory


class FormDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, title=None):

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
        bb.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self._onOk)
        bb.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self._onCancel)

    @property
    def Ok(self):
        '''Returns a reference to the Dialog Ok button to connect its signals'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)

    @property
    def Cancel(self):
        '''Returns a reference to the Dialog Cancel button to connect its signals'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)

    def _onOk(self):
        '''Saves the widget states and calls `onOk`'''
        self.saveAllWidgetStates()
        self.onOk()
        self.close()

    def _onCancel(self):
        '''Calls `onCancel`, closes the FormDialog and restores the previously saved states
        or the default states.'''
        self.onCancel()
        self.close()
        self.restoreAllSavedWidgetStates()

    def onOk(self):
        '''Called when the dialog's "Ok" button is clicked.
        Can be redefined to add additional functionality on "Ok"'''
        pass

    def onCancel(self):
        '''Called when the dialog's "Cancel" button is clicked.
        Can be redefined to add additional functionality on "Cancel"'''
        pass

    @property
    def widgets(self):
        return self.formWidget.widgets

    @property
    def groupBox(self):
        return self.formWidget.groupBox

    def addWidget(self, qwidget, qlabel=None, name=None, layout='form'):
        '''
        Adds a qwidget (and a qlabel widget) in the (same row of the) layout.
        layout = 'form' - adds to the FormLayout
        layout = 'vertical' - adds to the Vertical layout below the form.
        To add to the form layout, qlabel and name must be passed.
        '''
        if layout == 'vertical':
            if name is not None or qlabel is not None:
                raise ValueError('`qlabel` and `name` are unsupported when `layout=vertical`')
            self.formWidget.uiElements['verticalLayout'].addWidget(qwidget)
        elif layout == 'form':
            if name is None:
                raise ValueError('To add the widget to the form, please set name.')
            if qlabel is None:
                raise ValueError('To add the widget to the form, please set label.')
            self.formWidget.addWidget(qwidget, qlabel, name)
        else:
            raise ValueError(f"layout '{layout}' unrecognised: expected 'form' or 'vertical'")

    def addSpanningWidget(self, qwidget, name=None, layout='form'):
        '''
        Adds a spanning qwidget occupying the full row in the layout.
        layout = 'form' - adds the widget to the FormLayout
        layout = 'vertical' - adds the widget to the Vertical layout below the form.
        To add to the form layout, name must be passed.
        '''
        if layout == 'vertical':
            if name is not None:
                raise ValueError(f"`name='{name}'` cannot be given if `layout='{layout}'`")
            self.formWidget.uiElements['verticalLayout'].addWidget(qwidget)
        elif layout == 'form':
            if name is None:
                raise ValueError('To add the widget to the form, please set name')
            self.formWidget.addSpanningWidget(qwidget, name)
        else:
            raise ValueError(
                f"layout {layout} is not recognised, must be set to 'form' or 'vertical'")

    def insertWidgetToFormLayout(self, row, name, qwidget, qlabel=None):
        '''
        Inserts a widget and a label widget, or a spanning widget if 'qlabel' is None, to the form layout, `groupBoxFormLayout`,
        in the position specified by row. If row is out of bounds, the widget is added at the end.
        It adds to the widget dictionary and the default states 
        dictionary.

        Parameters:
        ----------
        row: int
        name: str
        qwidget: qwidget
        qlabel: qlabel widget or str
        '''
        self.formWidget.insertWidgetToFormLayout(row, name, qwidget, qlabel)

    def insertWidgetToVerticalLayout(self, row, qwidget):
        '''
        Inserts a widget to the vertical layout at position specified by row.
        '''
        self.formWidget.uiElements['verticalLayout'].insertWidget(row, qwidget)

    def removeWidgetFromVerticalLayout(self, qwidget):
        '''
        Removes a widget from the vertical layout.
        '''
        self.formWidget.uiElements['verticalLayout'].removeWidget(qwidget)
        qwidget.setParent(None)

    def getWidgetFromVerticalLayout(self, index):
        return self.formWidget.uiElements['verticalLayout'].itemAt(index).widget()

    def removeWidget(self, name):
        '''
        If not present already, creates a dictionary to store the removed qwidgets.
        Sets the parent of the qwidget (and qlabel if present) to `None` and 
        stores the widgets in the removed-widgets dictionary.
        Deletes the row in the form layout.
        Deletes the qwidget and qlabel from the widgets dictionary.
        Deletes the widget number from the widget-number dictionary.
    
        Parameters:
        --------------
        name : str
            name of the widget to be removed
        '''
        self.formWidget.removeWidget(name)

    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.formWidget.getNumWidgets()

    def getWidget(self, name, role='field'):
        '''Returns the Widget by the name with which it has been added

        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label

        Raises ValueError if the role is not field or label.
        '''
        return self.formWidget.getWidget(name, role)

    def getWidgets(self):
        '''Returns a dictionary of the widgets currently present in the form.'''
        return self.formWidget.getWidgets()

    def getRemovedWidgets(self):
        '''Returns the dictionary of the removed widgets previously present in the form.'''
        return self.formWidget.getRemovedWidgets()

    def getWidgetNumber(self, name):
        '''Returns the widget number by the widget name.'''
        return self.formWidget.getWidgetNumber(name)


    def getWidgetNumberDictionary(self):
        '''Returns the widget number dictionary.'''
        return self.formWidget.getWidgetNumberDictionary()

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
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.formWidget.saveAllWidgetStates()

    def getWidgetStates(self):
        '''Returns the saved widget states.'''
        self.formWidget.getWidgetStates()

    def restoreAllSavedWidgetStates(self):
        '''
        Restore all widgets in the form to the state saved by `saveAllWidgetStates()`.
        If `saveAllWidgetStates()` method was not previously invoked, do nothing.
        '''
        self.formWidget.restoreAllSavedWidgetStates()

    def getAllWidgetStates(self):
        '''
        Returns
        -------
        states: dict
          Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool},
                   ...},
          e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True},
                 'widget2': {'value': 2, 'enabled': False, 'visible': False}}.
        '''
        return self.formWidget.getAllWidgetStates()

    def getWidgetState(self, widget, role=None):
        '''
        Parameters
        ----------
        widget: QWidget or str
            The widget or its name (or its name + '_field' or '_label', when role is None) to get the state of.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to. This is used only if `widget` is the widget name string.

        Returns
        -------
        state: dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int},
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
            This can be used to restore the state of the widget using `setWidgetState()`.
        '''
        return self.formWidget.getWidgetState(widget, role)

    def applyWidgetState(self, name, state, role=None):
        '''
        Applies the given `state` to the widget associated with `name` and `role`. 
        If role is None, the role is assigned to be 'field'.

        Parameters
        ----------
        name: str
            The name of the widget to apply the state to. 
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to.
        state: dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int},
                    e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
        '''
        return self.formWidget.applyWidgetState(name, state, role)

    def applyWidgetStates(self, state):
        '''
        Removes the widgets in the form which are not present in the states. 
        If the widgets in the states are not present in the form, 
        they are retrieved from the removed-widgets dictionary and inserted at position 
        given by the widget number recorded in the states. An error is raised when the 
        widget in thet state is not in the form nor in the removed widgets.
        Applies the given states to the form's widgets.

        Parameters
        ----------
        states: nested_dict
          Format: {'name_field': {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int},
                    'name_label': {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int}, ...},
                  e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0},
                  'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number' : 1}}.
        '''
        return self.formWidget.applyWidgetStates(state)
