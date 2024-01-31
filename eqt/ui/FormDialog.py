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
        '''Returns a reference to the Dialog Ok button to connect its signals.'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)

    @property
    def Cancel(self):
        '''Returns a reference to the Dialog Cancel button to connect its signals.'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)

    def _onOk(self):
        '''Saves the widget states and calls `onOk`.'''
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
        Can be redefined to add additional functionality on "Ok".'''
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
        Adds a widget to the layout. In particular, adds a qwidget and a qlabel widget
        in the same row of the form layout if layout is 'form' and adds a spanning widget
        to the vertical layout if layout is 'vertical'.

        Parameters
        ----------
        qwidget: widget
        qlabel: qlabel widget or str
            Only supported for layout='form'.
        name: str
            Only supported for layout='form'.
        layout: 'form' or 'vertical'
            'form' adds to the `FormLayout`, 'vertical' adds to the `VerticalLayout` below
            the form.
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
        Adds a widget spanning the full row in the layout.

        Parameters
        ----------
        name: str
            Required for `layout='form'`.
        layout: 'form' or 'vertical'
            'form': adds the widget to the `FormLayout` (requires `name`).
            'vertical': adds the widget to the `VerticalLayout` below the form.
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
        Inserts a labelled widget, or a spanning widget, to the form layout.
        The position in the form is specified by row. If row is out of bounds, the widget
        is added at the end of the form. An error is raised if `name` is already in use
        by another widget in the form. The entries associated with the widget are added
        to the widget dictionary and the default-widget-states
        dictionary.

        Parameters:
        ----------
        row: int
            The position in the form where the widget is added.
        name: str
            The string associated to the qwidget and qlabel.
        qwidget: widget
            The widget to be added on the right hand side of the form or as a spanning widget.
        qlabel: qlabel widget or str
            The qlabel widget, or a str from which a qlabel widget is created, to be added
            on the left hand side of the form. If qlabel is `None` the widget spans the full
            width of the form.
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
        '''
        Returns the widget in the vertical layout located at position index.
        '''
        return self.formWidget.uiElements['verticalLayout'].itemAt(index).widget()

    def removeWidget(self, name):
        '''
        Removes the widget with the specified name from the form layout.
        This method delete the qwidget, and qlabel if present, from the widgets dictionary
        and sets their parent to `None`.

        Parameters
        ----------
        name: str
            The name of the widget to be removed.

        Returns
        -------
        tuple or QWidget
            If the widget has a corresponding label, a tuple containing the widget
            and label is returned. Otherwise, only the widget is returned.
        '''
        self.formWidget.removeWidget(name)

    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.formWidget.getNumWidgets()

    def getWidget(self, name, role='field'):
        '''
        Returns the widget by the name with which it has been added.
        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label.
        Raises ValueError if the role is not field or label.
        '''
        return self.formWidget.getWidget(name, role)

    def getWidgets(self):
        '''Returns a dictionary of the widgets currently present in the form.'''
        return self.formWidget.getWidgets()

    def getWidgetNumber(self, name, role='field'):
        '''
        Returns the widget number by the widget name.
        This is the row of the widget in the form layout.
        '''
        return self.formWidget.getWidgetNumber(name, role)

    def setWidgetVisible(self, name, visible):
        '''
        Sets the visibility of the named widget (and associated label).
        '''
        self.formWidget.setWidgetVisible(name, visible)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets currently present in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.formWidget.saveAllWidgetStates()

    def getWidgetStates(self):
        '''Returns the saved widget states.'''
        return self.formWidget.getWidgetStates()

    def getDefaultWidgetStates(self):
        '''Returns the saved default widget states.'''
        return self.formWidget.getDefaultWidgetStates()

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
            Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
                     'widget_number': int}, ...},
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number': 0},
                  'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number': 1}}.
        '''
        return self.formWidget.getAllWidgetStates()

    def getWidgetState(self, widget, role=None):
        '''
        Returns the current state of the widget in the form.

        Parameters
        ----------
        widget: QWidget or str
            The widget or its name (or its name + '_field' or '_label', when role is None) to get
            the state of.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to. This is used only if `widget` is the
            widget name string.

        Returns
        -------
        state: dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool,
                     'widget_number' : int},
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
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool,
                     'widget_number' : int},
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
        '''
        return self.formWidget.applyWidgetState(name, state, role)

    def applyWidgetStates(self, states):
        '''
        Applies the given states to the form's widgets. It raises an error if the keys in the
        dicitonary of states and the keys in the dictionary of widgets in the form are not the
        same.

        Parameters
        ----------
        states: dict
            Format: {'name_field': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
                     'widget_number' : int}, 'name_label': {'value': str | bool | int,
                     'enabled': bool, 'visible': bool, 'widget_number' : int}, ...}.
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number': 0},
                  'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number': 1}}.
        '''
        return self.formWidget.applyWidgetStates(states)
