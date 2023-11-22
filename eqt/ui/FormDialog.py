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
        bb.button(QtWidgets.QDialogButtonBox.Cancel).clicked.connect(self._onCancel)

    @property
    def Ok(self):
        '''returns a reference to the Dialog Ok button to connect its signals'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok)

    @property
    def Cancel(self):
        '''returns a reference to the Dialog Cancel button to connect its signals'''
        return self.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel)

    def _onCancel(self):
        '''calls onCancel and closes the FormDialog'''
        self.onCancel()
        self.close()

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
        Adds a widget to the layout.
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
        Adds a spanning widget to the layout.
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
        '''Invokes `insertWidgetToFormLayout` in `UIFormWidget`.'''
        self.formWidget.insertWidgetToFormLayout(row, name, qwidget, qlabel)

    def insertWidgetToVerticalLayout(self, row, qwidget):
        '''
        Inserts a widget to the vertical layout at position specified by row.
        '''
        self.formWidget.uiElements['verticalLayout'].insertWidget(row, qwidget)

    def removeWidget(self, name):
        '''
        Removes a widget (and its label if present) from the layout.
        Decreases the counter for the number of widgets in the layout.
        Deletes the field (and label) from the dictionary.
        '''
        self.formWidget.removeWidget(name)

    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.formWidget.getNumWidgets()

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
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.formWidget.saveAllWidgetStates()

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
            The (name of) widget to get the state of.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to get the state of (only if `widget` is a `str`).
            If unspecified, the widget is chosen based on `name=widget`.

        Returns
        -------
        dict
            Widget state, format: {'value': str | bool | int, 'enabled': bool, 'visible': bool},
            e.g. {'value': 1, 'enabled': True, 'visible': True}.
            This can be used to restore the state of the widget using `setWidgetState()`.
        '''
        return self.formWidget.getWidgetState(widget, role)

    def applyWidgetState(self, name, state, role=None):
        '''
        Applies the given state to the widget with the given name.

        Parameters
        ----------
        name: str
            The name of the widget to apply the state to.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to.
            If unspecified, the widget is chosen based on `name`.
        state: dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool},
            e.g. {'value': 1, 'enabled': True, 'visible': True}.
        '''
        return self.formWidget.applyWidgetState(name, state, role)

    def applyWidgetStates(self, state):
        '''
        Applies the given states to the form's widgets.

        Parameters
        ----------
        state: dict
          Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool},
                   ...},
          e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True},
                 'widget2': {'value': 2, 'enabled': False, 'visible': False}}.
        '''
        return self.formWidget.applyWidgetStates(state)
