from PySide2 import QtCore, QtWidgets

from . import UIFormFactory


class FormDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, title=None):
        super().__init__(parent)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok
                                                    | QtWidgets.QDialogButtonBox.Cancel)
        self.formWidget = UIFormFactory.getQWidget(parent=self)
        # set the layout of the dialog
        self.setLayout(self.formWidget.uiElements['verticalLayout'])

        if title is not None:
            self.setWindowTitle(title)
        # add button box to the UI
        self.formWidget.uiElements['verticalLayout'].addWidget(self.buttonBox)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).clicked.connect(self._onOk)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self._onCancel)

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
        qwidget : QWidget
        qlabel : qlabel widget or str
            only supported when layout is 'form'
        name : str
            only supported when layout is 'form'
        layout : 'form' or 'vertical'
                'form' - adds to the `groupBoxFormLayout`,
                'vertical' - adds to the `verticalLayout` below the form.
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
        Adds a spanning widget occupying the full row in the layout.

        Parameters
        ----------
        qwidget : QWidget
        name : str
            only supported when layout is 'form'
        layout : 'form' or 'vertical'
                'form' - adds to the `groupBoxFormLayout`,
                'vertical' - adds to the `verticalLayout` below the form.
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

    def insertWidget(self, row, name, qwidget, qlabel=None):
        '''
        Inserts a labelled widget, or a spanning widget, to the form layout.
        The position in the form is specified by row. If row is out of bounds, the widget
        is added at the end of the form. An error is raised if `name` is already in use
        by another widget in the form. The entries associated with the widget are added
        to the widget dictionary and the default-widget-states
        dictionary.

        Parameters
        ----------
        row : int
            The position in the form where the widget is added.
        name : str
            The string associated to the qwidget and qlabel.
        qwidget : QWidget
            The widget to be added on the right hand side of the form or as a spanning widget.
        qlabel : qlabel widget or str
            The qlabel widget, or a str from which a qlabel widget is created, to be added
            on the left hand side of the form. If qlabel is `None` the widget spans the full
            width of the form.
        '''
        self.formWidget.insertWidget(row, name, qwidget, qlabel)

    def insertWidgetToVerticalLayout(self, row, qwidget):
        '''Inserts a widget to the vertical layout at position specified by row.'''
        self.formWidget.uiElements['verticalLayout'].insertWidget(row, qwidget)

    def getWidgetFromVerticalLayout(self, index):
        '''Returns the widget in the vertical layout located at position index.'''
        return self.formWidget.uiElements['verticalLayout'].itemAt(index).widget()

    def getIndexFromVerticalLayout(self, widget):
        '''
        Returns the index of the widget in the vertical layout.

        Parameters
        -------------
        widget : QWidget
            The widget in the layout.

        Return
        ------------
        int
            The index of the widget in the layout.
        '''
        return self.formWidget.uiElements['verticalLayout'].indexOf(widget)

    def removeWidget(self, name):
        '''
        Removes the widget with the specified name from the form layout.
        This method deletes the qwidget, and qlabel if present, from the widgets dictionary
        and sets their parent to `None`.

        Parameters
        ----------
        name : str
            The name of the widget to be removed.

        Returns
        -------
        tuple or QWidget
            If the widget has a corresponding label, a tuple containing the widget
            and label is returned. Otherwise, only the widget is returned.
        '''
        return self.formWidget.removeWidget(name)

    def removeWidgetFromVerticalLayout(self, widget):
        '''Removes a widget from the vertical layout.

        Parameters
        ----------
        widget : QWidget
            The widget to be removed.
        '''
        self.formWidget.uiElements['verticalLayout'].removeWidget(widget)
        widget.setParent(None)
        return widget

    def getNumWidgets(self):
        '''Returns the number of widgets in the form.'''
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

    def getWidgetRow(self, name, role='field'):
        '''
        Returns the widget row in the form layout by the widget name.
        This is the row of the widget in the form layout.
        '''
        return self.formWidget.getWidgetRow(name, role)

    def setWidgetVisible(self, name, visible):
        '''
        Sets the visibility of the widget and associated label with the given name.

        Parameters
        ----------
        name : str
            The name of the widget to set visible/invisible
        visible : bool
            True to set the widget visible, False to hide it
        '''
        self.formWidget.setWidgetVisible(name, visible)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets currently present in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.formWidget.saveAllWidgetStates()

    def getWidgetStates(self):
        '''Deprecated. Use `getSavedWidgetStates`.'''
        return self.formWidget.getWidgetStates()

    def getSavedWidgetStates(self):
        '''Returns the saved widget states.'''
        return self.formWidget.getSavedWidgetStates()

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
        dict
            Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_row': int}, ...}.
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_row': 0},
            'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_row': 1}}.
        '''
        return self.formWidget.getAllWidgetStates()

    def getWidgetState(self, widget, role=None):
        '''
        Returns the current state of the widget in the form.

        Parameters
        ----------
        widget : QWidget or str
            The widget or its name (or its name + '_field' or '_label', when role is None) to get
            the state of.
        role : str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to. This is used only if `widget` is the
            widget name string.

        Returns
        -------
        state : dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_row' : int}.
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_row' : 0}.
            This can be used to restore the state of the widget using `setWidgetState()`.
        '''
        return self.formWidget.getWidgetState(widget, role)

    def applyWidgetState(self, name, state, role=None):
        '''
        Applies the given `state` to the widget associated with `name` and `role`.
        If role is None, the role is assigned to be 'field'.

        Parameters
        ----------
        name : str
            The name of the widget to apply the state to.
        role : str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to.
        state : dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_row' : int}.
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_row' : 0}.
        '''
        return self.formWidget.applyWidgetState(name, state, role)

    def applyWidgetStates(self, states):
        '''
        Applies the given states to the form's widgets. It raises an error if the keys in the
        dicitonary of states and the keys in the dictionary of widgets in the form are not the
        same.

        Parameters
        ----------
        states : dict
            Format: {'name_field': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_row' : int}, 'name_label': {'value': str | bool | int, 'enabled': bool,
            'visible': bool, 'widget_row' : int}, ...}.
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_row': 0},
                  'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_row': 1}}.
        '''
        return self.formWidget.applyWidgetStates(states)


class AdvancedFormDialog(FormDialog):
    def __init__(self, parent=None, title=None, parent_button_name=None):
        """
        Constructs an advanced form dialog that adds widgets on its parent.

        To add widgets to the parent, call `displayWidgetValueOnParent` after creating an instance
        of the class. The advanced form dialog has a default button in its vertical layout, which
        is located between the form layout and the buttons 'ok' and 'cancel'. This button sets the
        widgets to their default values.

        Parameters
        ----------
        parent : UIFormWidget or None, optional
            The parent widget of the advanced form dialog.
            If None, the dialog is created without a parent.
        title : str or None, optional
            The title of the advanced form dialog.
        parent_button_name : str or None, optional
            The name of the button opening the advanced form dialog in the parent.
            If passed, the extra widgets will be added under this button in the parent,
            otherwise they are added at the end.
        """
        self.dialog_parent = parent
        self.display_on_parent = []
        if parent_button_name is None:
            self.parent_button_row = -1
        elif parent is None:
            raise ValueError(
                'The parent is None. Set the parent if you want to set the parent button name.')
        else:
            self.parent_button_row = self.dialog_parent.getWidgetRow(parent_button_name)

        FormDialog.__init__(self, parent, title)

        # add default button to vertical layout
        self.default_button = QtWidgets.QPushButton("Set default values")
        self.insertWidgetToVerticalLayout(1, self.default_button)
        self.default_button.clicked.connect(lambda: self._setDefaultValues())

    def _onOk(self):
        """
        Called when the "Ok" button is clicked in the advanced dialog.

        Calls the super-class method `_onOk`, sets the default widgets
        to visible, and adds/updates/removes widgets from the
        parent depending on the the widgets in the advanced dialog.
        """
        super()._onOk()
        self.formWidget.setDefaultWidgetStatesVisibleTrue()
        if self.display_on_parent:
            if self.getSavedWidgetStates() == self.getDefaultWidgetStates():
                self._removeWidgetsFromParent()
            else:
                self._addOrUpdateWidgetsInParent()

    def _addOrUpdateWidgetsInParent(self):
        """
        Adds or updates widgets in the parent form.

        This method iterates over the display_on_parent and adds the widgets to the parent
        form. If a widget already exists in the parent form, it is updated with the most current
        value set in the advanced dialog.
        """
        for index, name in enumerate(self.display_on_parent, start=1):
            widget_row = self.parent_button_row + index if self.parent_button_row != -1 else -1
            value = self.getSavedWidgetStates()[f'{name}_field']['value']
            qwidget = self.getWidget(name, 'field')
            if isinstance(qwidget, QtWidgets.QComboBox):
                value = qwidget.itemText(value)
            if f'{name}_field' not in self.dialog_parent.getWidgets():
                label = str(self.getSavedWidgetStates()[f'{name}_label']['value'])
                self.dialog_parent.insertWidget(widget_row, name, QtWidgets.QLabel(str(value)),
                                                label)
            else:
                self.dialog_parent.getWidget(name, 'field').setText(str(value))

    def _removeWidgetsFromParent(self):
        """
        Removes widgets from the parent form.

        This method iterates over the display_on_parent and removes
        the widgets from the parent.
        """
        for name in self.display_on_parent:
            if f'{name}_field' in self.dialog_parent.getWidgets():
                self.dialog_parent.removeWidget(name)

    def _setDefaultValues(self):
        """
        Sets the widgets in the advanced dialog to their default states.

        Makes the default widget states visible, as often the default states are saved while the
        widgets are not visible. Applies the widget states to the widgets in the form.
        """
        self.formWidget.setDefaultWidgetStatesVisibleTrue()
        self.applyWidgetStates(self.formWidget.default_widget_states)

    def displayWidgetValueOnParent(self, name):
        """
        Adds `name` in a list. The order in which names are added to this
        list reflects the order in which the widgets are added to the parent.
        Raises an error if the parent of the advanced dialog is `None`.

        Parameters
        ----------
        name : str
            The name of the widget in the advanced dialog to be displayed in the parent.
        """
        if self.dialog_parent is None:
            raise KeyError('''The advanced-dialog parent is None.
                           Set the parent if you want to add widgets to it.''')
        self.display_on_parent.append(name)
