from PySide2 import QtWidgets

from .UISliderWidget import UISliderWidget


class UIFormWidget:
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

        self.uiElements = {
            'verticalLayout': verticalLayout, 'groupBox': groupBox,
            'groupBoxFormLayout': groupBoxFormLayout}
        self.widgets = {}

    @property
    def num_widgets(self):
        return self.uiElements['groupBoxFormLayout'].rowCount()

    @property
    def groupBox(self):
        return self.uiElements['groupBox']

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
        if f'{name}_field' in self.widgets.keys():
            raise ValueError(f'''The name of widget you are trying to insert, {name},
                             is used already. Choose another name.''')

        formLayout = self.uiElements['groupBoxFormLayout']

        if qlabel is not None:
            if isinstance(qlabel, str):
                txt = qlabel
                qlabel = QtWidgets.QLabel(self)
                qlabel.setText(txt)
            formLayout.insertRow(row, qlabel, qwidget)
        else:
            formLayout.insertRow(row, qwidget)
        self._addToWidgetDictionary(self.widgets, name, qwidget, qlabel)
        self._addToDefaultWidgetStatesDictionary(name)

    def _addToWidgetDictionary(self, dictionary, name, qwidget, qlabel=None):
        '''Adds the field, and label if present, in the widget dictionary.'''
        dictionary[f'{name}_field'] = qwidget
        if qlabel is not None:
            dictionary[f'{name}_label'] = qlabel

    def _popWidgetFromDictionary(self, dictionary, name):
        '''
        Removes the item(s) associated with `name` from a dictionary.

        Parameters:
        -----------------
        dictionary : dict
            The dictionary from which to remove the items.
        name : str
            The name of the item(s) to be removed.

        Returns:
        -------
        qwidget : QWidget
            The removed widget associated with `name`, if it exists in the dictionary.

        qlabel : QLabel, optional
            The removed label associated with `name`, if it exists in the dictionary.

        Raises:
        ------
        KeyError
            If no widget associated with the dictionary key `name` or `{name}_field` is found.

        '''
        if name in dictionary.keys():
            qwidget = dictionary.pop(name)
        elif f'{name}_field' in dictionary.keys():
            qwidget = dictionary.pop(f'{name}_field')
        else:
            raise KeyError(
                f'No widget associated with the dictionary key `{name}` or `{name}_field`.')
        if f'{name}_label' in dictionary.keys():
            qlabel = dictionary.pop(f'{name}_label')
            return qwidget, qlabel
        else:
            return qwidget

    def addWidget(self, qwidget, qlabel, name):
        '''
        Adds a widget and a label widget at the the end of
        the form layout.

        Parameters:
        ----------
        qwidget: widget
            The widget to be added on the right hand side of the form.
        qlabel: qlabel widget or str
            The qlabel widget, or a str from which a qlabel widget is created, to be added
            on the left hand side of the form.
        name: str
            The string associated to the qwidget and qlabel.
        '''
        self.insertWidgetToFormLayout(-1, name, qwidget, qlabel)

    def addSpanningWidget(self, qwidget, name):
        '''
        Adds a spanning qwidget occupying the full row in the form layout.

        Parameters:
        ----------
        qwidget: widget
            The widget to be added on the form.
        name: str
            The string associated to the qwidget.
        '''
        self.insertWidgetToFormLayout(-1, name, qwidget)

    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.num_widgets

    def removeWidget(self, name):
        '''
        Removes the widget with the specified name from the form layout.
        This method delete the qwidget, and qlabel if present, from the widgets dictionary
        and sets their parent to `None`.

        Parameters:
        --------------
        name : str
            The name of the widget to be removed.

        Returns:
        --------------
        tuple or QWidget
            If the widget has a corresponding label, a tuple containing the widget
            and label is returned. Otherwise, only the widget is returned.
        '''
        widget_number = self.getWidgetNumber(name)
        if f'{name}_label' in self.getWidgets().keys():
            self.getWidget(name, 'label').setParent(None)
            qwidget, qlabel = self._popWidgetFromDictionary(self.getWidgets(), name)
            self.uiElements['groupBoxFormLayout'].removeRow(widget_number)
            return qwidget, qlabel
        self.getWidget(name, 'field').setParent(None)
        qwidget = self._popWidgetFromDictionary(self.getWidgets(), name)
        self.uiElements['groupBoxFormLayout'].removeRow(widget_number)
        return qwidget

    def getWidget(self, name, role='field'):
        '''
        Returns the widget by the name with which it has been added.
        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label.
        Raises ValueError if the role is not field or label.
        '''
        allowed_roles = 'field', 'label'
        if role in allowed_roles:
            return self.widgets[f'{name}_{role}']
        raise ValueError(f'Unexpected role: expected any of {allowed_roles}, got {role}')

    def getWidgetNumber(self, name, role='field'):
        '''
        Returns the widget number by the widget name.
        This is the row of the widget in the form layout.
        '''
        return self.uiElements['groupBoxFormLayout'].getWidgetPosition(self.getWidget(name,
                                                                                      role))[0]

    def setWidgetVisible(self, name, visible):
        '''
        Sets the visibility of the widget and associated label with the given name.

        Parameters
        ----------
        name: str
            The name of the widget to set visible/invisible
        visible: bool
            True to set the widget visible, False to hide it
        '''
        allowed_roles = ['field', 'label']
        for role in allowed_roles:
            try:
                self.getWidget(name, role).setVisible(visible)
            except Exception:
                # We may not have a label for the widget
                pass

    def getWidgets(self):
        '''Returns a dictionary of the widgets currently present in the form.'''
        return self.widgets

    def addTitle(self, qlabel, name):
        if isinstance(qlabel, str):
            txt = qlabel
            qlabel = QtWidgets.QLabel(self.uiElements['groupBox'])
            qlabel.setText(txt)
        qlabel.setStyleSheet("font-weight: bold")
        self.insertWidgetToFormLayout(-1, name, qlabel)

    def addSeparator(self, name):
        # Adds horizontal separator to the form
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.HLine)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.insertWidgetToFormLayout(-1, name, frame)

    def _addToDefaultWidgetStatesDictionary(self, name):
        '''
        If not present already, creates an attribute dictionary of default widget states. The
        entries are in the format: {'value': str | bool | int, 'enabled': bool, 'visible': bool,
        'widget_number': int}. This can be used to restore the default states of the widgets
        invoking `applyWidgetStates`.
        '''
        if not hasattr(self, 'default_widget_states'):
            self.default_widget_states = {}
        # add the default state of the qwidget
        self.default_widget_states[f'{name}_field'] = self.getWidgetState(name, 'field')
        # add the default state of the qlabel
        if f'{name}_label' in self.widgets.keys():
            self.default_widget_states[f'{name}_label'] = self.getWidgetState(name, 'label')

    def setDefaultWidgetStatesVisibleTrue(self):
        '''
        Sets all of the entries 'visible' in the `default_widget_states` dictionary to be `True`.
        '''
        for key in self.default_widget_states.keys():
            self.default_widget_states[key]['visible'] = True

    def getAllWidgetStates(self):
        '''
        Returns
        -------
        dict
            Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_number': int}, ...}.
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number': 0},
            'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number': 1}}.
        '''
        all_widget_states = {}
        for key, widget in self.widgets.items():
            all_widget_states[key] = self.getWidgetState(widget)
        return all_widget_states

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
            'widget_number' : int}.
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
            This can be used to restore the state of the widget using `setWidgetState()`.
        '''
        if widget is None:
            raise ValueError('The widget or the name of widget must be given.')

        if isinstance(widget, str):
            if role is not None:
                if role not in ['label', 'field']:
                    raise ValueError(f'Role must be either "label", "field" or None. Got {role}.')
                name_role = widget + '_' + role
                name = widget
            else:
                name, role = self._getNameAndRoleFromKey(widget)
                name_role = name + '_' + role

            try:
                widget = self.widgets[name_role]
            except KeyError:
                raise KeyError(f'No widget associated with the dictionary key `{name_role}`.')
        else:
            name, role = self._getNameAndRoleFromWidget(widget)
        widget_state = {}
        widget_state['enabled'] = widget.isEnabled()
        widget_state['visible'] = widget.isVisible()

        if isinstance(widget, QtWidgets.QLabel):
            widget_state['value'] = widget.text()
        elif isinstance(widget, (QtWidgets.QCheckBox, QtWidgets.QPushButton)):
            widget_state['value'] = widget.isChecked()
        elif isinstance(widget, QtWidgets.QComboBox):
            widget_state['value'] = widget.currentIndex()
        elif isinstance(widget, UISliderWidget) or isinstance(widget, QtWidgets.QSlider):
            widget_state['value'] = widget.value()
        elif isinstance(widget, (QtWidgets.QDoubleSpinBox, QtWidgets.QSpinBox)):
            widget_state['value'] = widget.value()
        elif isinstance(widget, QtWidgets.QLineEdit):
            widget_state['value'] = widget.text()
        elif isinstance(widget, QtWidgets.QRadioButton):
            widget_state['value'] = widget.isChecked()
        elif isinstance(widget, (QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
            widget_state['value'] = widget.toPlainText()

        widget_state['widget_number'] = self.getWidgetNumber(name, role)
        return widget_state

    def _getNameAndRoleFromKey(self, key):
        '''
        Given a key, returns the name and the role.
        Role can be extracted as the suffix to key or is set as `field` by default.

        Parameters
        -------------
        key: str
            Format: name or name_field or name_label
        '''
        if key.endswith('_field'):
            name = key.removesuffix('_field')
            role = 'field'
        elif key.endswith('_label'):
            name = key.removesuffix('_label')
            role = 'label'
        else:
            name = key
            role = 'field'
        return name, role

    def _getNameAndRoleFromWidget(self, widget):
        '''
        Given a widget, finds it in the widget dictionary and returns its name and role.

        Parameters
        -------------
        widget: qwidget
        '''
        for key, value in self.widgets.items():
            if value == widget:
                name, role = self._getNameAndRoleFromKey(key)
        return name, role

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
            'widget_number' : int}.
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
        '''
        if role is not None:
            if role in ['label', 'field']:
                name_role = name + '_' + role
            else:
                raise ValueError(f'Role must be either "label", "field" or None. Got {role}.')
        else:
            name_role = f'{name}_field'

        # retrieve widget
        try:
            widget = self.widgets[name_role]
        except KeyError:
            raise KeyError(f'No widget associated with the dictionary key `{name_role}`.')
        # apply state
        for key, value in state.items():
            if key == 'enabled':
                widget.setEnabled(value)
            elif key == 'visible':
                widget.setVisible(value)
            elif key == 'value':
                if isinstance(widget, QtWidgets.QLabel):
                    widget.setText(value)
                elif isinstance(widget, QtWidgets.QCheckBox):
                    widget.setChecked(value)
                elif isinstance(widget, QtWidgets.QComboBox):
                    widget.setCurrentIndex(value)
                elif isinstance(widget, (UISliderWidget, QtWidgets.QSlider)):
                    widget.setValue(value)
                elif isinstance(widget, (QtWidgets.QDoubleSpinBox, QtWidgets.QSpinBox)):
                    widget.setValue(value)
                elif isinstance(widget, QtWidgets.QPushButton):
                    widget.setChecked(value)
                elif isinstance(widget, QtWidgets.QLineEdit):
                    widget.setText(value)
                elif isinstance(widget, QtWidgets.QRadioButton):
                    widget.setChecked(value)
                elif isinstance(widget, (QtWidgets.QTextEdit, QtWidgets.QPlainTextEdit)):
                    widget.setPlainText(value)

    def applyWidgetStates(self, states):
        '''
        Applies the given states to the form's widgets. It raises an error if the keys in the
        dicitonary of states and the keys in the dictionary of widgets in the form are not the
        same.

        Parameters
        ----------
        states: nested_dict
            Format: {'name_field': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_number' : int}, 'name_label': {'value': str | bool | int, 'enabled': bool,
            'visible': bool, 'widget_number' : int}, ...}.
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0},
            'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number' : 1}}.
        '''
        if self.widgets.keys() != states.keys():
            raise KeyError(f'''The widgets in the form are {self.widgets.keys()} whereas
                           the widgets in the states are {states.keys()}. These must be
                           equal for the states to be applied to the form.''')
        for key, widget_state in states.items():
            name, role = self._getNameAndRoleFromKey(key)
            self.applyWidgetState(name, widget_state, role)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets currently present in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.widget_states = self.getAllWidgetStates()

    def getWidgetStates(self):
        '''Returns the saved widget states.'''
        return self.widget_states

    def getDefaultWidgetStates(self):
        '''Returns the saved default widget states.'''
        return self.default_widget_states

    def restoreAllSavedWidgetStates(self):
        '''
        All widgets in the form are restored to the saved states. There are saved states only if
        `saveAllWidgetStates` was previously invoked. If there are no previously saved states,
        `default_widget_states` are used instead, after being made visible.
        '''
        if not hasattr(self, 'widget_states'):
            self.setDefaultWidgetStatesVisibleTrue()
            self.applyWidgetStates(self.default_widget_states)
        else:
            self.applyWidgetStates(self.widget_states)


class FormWidget(QtWidgets.QWidget, UIFormWidget):
    def __init__(self, parent=None):
        # dockWidgetContents = QtWidgets.QWidget()

        QtWidgets.QWidget.__init__(self, parent)
        self.createForm()


class FormDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None, title=None):
        if title is None:
            title = ''
        QtWidgets.QDockWidget.__init__(self, title, parent)
        widget = FormWidget(parent)
        self.setWidget(widget)
        if title is not None:
            self.setObjectName(title)

    def addWidget(self, qwidget, qlabel, name):
        '''
        Adds a widget and a label widget at the the end of
        the form layout.

        Parameters:
        ----------
        qwidget: widget
            The widget to be added on the right hand side of the form.
        qlabel: qlabel widget or str
            The qlabel widget, or a str from which a qlabel widget is created, to be added
            on the left hand side of the form.
        name: str
            The string associated to the qwidget and qlabel.
        '''
        self.widget().addWidget(qwidget, qlabel, name)

    def addSpanningWidget(self, qwidget, name):
        '''
        Adds a spanning qwidget occupying the full row in the form layout.

        Parameters:
        ----------
        qwidget: widget
            The widget to be added on the form.
        name: str
            The string associated to the qwidget.
        '''
        self.widget().addSpanningWidget(qwidget, name)

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
        self.widget().insertWidgetToFormLayout(row, name, qwidget, qlabel)

    def removeWidget(self, name):
        '''
        Removes the widget with the specified name from the form layout.
        This method delete the qwidget, and qlabel if present, from the widgets dictionary
        and sets their parent to `None`.

        Parameters:
        --------------
        name : str
            The name of the widget to be removed.

        Returns:
        --------------
        tuple or QWidget
            If the widget has a corresponding label, a tuple containing the widget
            and label is returned. Otherwise, only the widget is returned.
        '''
        self.widget().removeWidget(name)

    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.widget().getNumWidgets()

    def getWidget(self, name, role='field'):
        '''
        Returns the widget by the name with which it has been added.
        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label.
        Raises ValueError if the role is not field or label.
        '''
        return self.widget().getWidget(name, role)

    def getWidgets(self):
        '''Returns a dictionary of the widgets currently present in the form.'''
        return self.widget().getWidgets()

    def getWidgetNumber(self, name, role='field'):
        '''
        Returns the widget number by the widget name.
        This is the row of the widget in the form layout.
        '''
        return self.widget().getWidgetNumber(name, role)

    def setWidgetVisible(self, name, visible):
        '''
        Sets the visibility of the widget and associated label with the given name.

        Parameters
        ----------
        name: str
            The name of the widget to set visible/invisible
        visible: bool
            True to set the widget visible, False to hide it
        '''
        self.widget().setWidgetVisible(name, visible)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets currently present in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.widget().saveAllWidgetStates()

    def getWidgetStates(self):
        '''Returns the saved widget states.'''
        return self.widget().getWidgetStates()

    def getDefaultWidgetStates(self):
        '''Returns the saved default widget states.'''
        return self.widget().getDefaultWidgetStates()

    def restoreAllSavedWidgetStates(self):
        '''
        All widgets in the form are restored to the saved states. There are saved states only if
        `saveAllWidgetStates` was previously invoked. If there are no previously saved states,
        `default_widget_states` are used instead, after being made visible.
        '''
        self.widget().restoreAllSavedWidgetStates()

    def getAllWidgetStates(self):
        '''
        Returns
        -------
        dict
          Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
          'widget_number': int},
                   ...},
          e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number': 0},
                 'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number': 1}}.
        '''
        return self.widget().getAllWidgetStates()

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
            'widget_number' : int}.
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
            This can be used to restore the state of the widget using `setWidgetState()`.
        '''
        return self.widget().getWidgetState(widget, role)

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
            'widget_number' : int}.
            e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
        '''
        return self.widget().applyWidgetState(name, state, role)

    def applyWidgetStates(self, states):
        '''
        Applies the given states to the form's widgets. It raises an error if the keys in the
        dicitonary of states and the keys in the dictionary of widgets in the form are not the
        same.

        Parameters
        ----------
        states: nested_dict
            Format: {'name_field': {'value': str | bool | int, 'enabled': bool, 'visible': bool,
            'widget_number' : int}, 'name_label': {'value': str | bool | int, 'enabled': bool,
            'visible': bool, 'widget_number' : int}, ...}.
            e.g. {'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0},
            'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number' : 1}}.
        '''
        return self.widget().applyWidgetStates(states)


class UIFormFactory(QtWidgets.QWidget):
    # def generateUIFormView(QtWidgets.QWidget):
    '''creates a widget with a form layout group to add things to

    basically you can add widget to the returned groupBoxFormLayout and paramsGroupBox
    The returned dockWidget must be added with
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    '''
    @staticmethod
    def getQDockWidget(parent=None, title=None):
        return FormDockWidget(parent, title)

    @staticmethod
    def getQWidget(parent=None):
        return FormWidget(parent)
