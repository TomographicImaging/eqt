import logging

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

        # number of widgets currently present in the groupBoxFormLayout
        self.num_widgets = 0
        # number of widgets removed from the groupBoxFormLayout
        self.num_removed_widgets = 0
        self.widget_number_dictionary = {}
        self.uiElements = {
            'verticalLayout': verticalLayout, 'groupBox': groupBox,
            'groupBoxFormLayout': groupBoxFormLayout}
        self.widgets = {}
        self.default_widgets = {}

    @property
    def groupBox(self):
        return self.uiElements['groupBox']

    def insertWidgetToFormLayout(self, row, name, qwidget, qlabel=None):
        '''
        Inserts a widget, and a label widget, or a spanning widget to the form layout, `groupBoxFormLayout`,
        in the position specified by row. If row is out of bounds, the widget is added at the end.
        It invokes `populate_widget_dictionaries` to populate the widget dictionary and the default states 
        dictionary.
        It increases "num_widgets" by 1 unit.
        It should not be used to move widgets in a form.

        Parameters:
        ----------
        row: int
        name: str
        qwidget: qwidget
        qlabel: qlabel widget or str
        '''
        formLayout = self.uiElements['groupBoxFormLayout']

        if qlabel is not None:
            if isinstance(qlabel, str):
                txt = qlabel
                qlabel = QtWidgets.QLabel(self)
                qlabel.setText(txt)
            self.uiElements['groupBoxFormLayout'].insertRow(row, qlabel, qwidget)
        else:
            self.uiElements['groupBoxFormLayout'].insertRow(row, qwidget)
        self.increaseNumWidgets() 
        self.populate_widget_dictionary(self.widgets, name, qwidget, qlabel)
        self.populate_widget_number_dictionary(name, row)
        self.populate_widget_dictionary(self.default_widgets, name, qwidget, qlabel)
        self.populate_default_widget_states_dictionary(name)

    def _addWidget(self, name, qwidget, qlabel=None):
        '''
        Adds a widget, and a label widget, or a spanning widget at the the end of
        the `groupBoxFormLayout` by invoking `insertWidgetToFormLayout`, where row is out of bounds. 

        Parameters:
        ----------
        name: str
        qwidget: widget
        qlabel: qlabel widget or str
        '''
        self.insertWidgetToFormLayout(-1, name, qwidget, qlabel)

    def populate_widget_dictionary(self, dictionary, name, qwidget, qlabel = None):
        """Adds the field (and label if present) in the widget dictionary.""" 
        dictionary[f'{name}_field'] = qwidget
        if qlabel is not None:
            dictionary[f'{name}_label'] = qlabel
        

    def populate_widget_number_dictionary(self, name, row):
        widget_number = row 
        if widget_number == -1:
            self.widget_number_dictionary[name] = self.num_widgets + self.num_removed_widgets - 1 
            print(self.widget_number_dictionary)
        else:
            for key, value in self.widget_number_dictionary.items():
                if value >= widget_number:
                    self.widget_number_dictionary[key] = value + 1
            self.widget_number_dictionary[name] = widget_number
            print(self.widget_number_dictionary)

    def pop_widget_number_dictionary(self, name, row):
        widget_number = row 
        for key, value in self.widget_number_dictionary.items():
            if value > widget_number:
                self.widget_number_dictionary[key] = value - 1
        self.widget_number_dictionary.pop(name) 
        print(self.widget_number_dictionary)

    def remove_widget_from_dictionary(self, dictionary, name):
        if f'{name}_field' in dictionary.keys():
            dictionary.pop(f'{name}_field')       # removes field from the dictionary
        if f'{name}_label' in dictionary.keys():
            dictionary.pop(f'{name}_label') 

    def addWidget(self, qwidget, qlabel, name):
        self._addWidget(name, qwidget, qlabel)
    
    def addSpanningWidget(self, qwidget, name):
        self._addWidget(name, qwidget)
        
    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.num_widgets

    def increaseNumWidgets(self):
        """Increases `num_widget` by 1 unit."""
        self.num_widgets += 1

    def decreaseNumWidgets(self):
        """Decreases `num_widget` by 1 unit."""
        self.num_widgets -= 1

    def removeWidget(self, name):
        '''
        Removes a widget (and its label if present) from the layout.
        Decreases the counter for the number of widgets in the layout.
        Deletes the field (and label) from the dictionary.
        '''
        formLayout = self.uiElements['groupBoxFormLayout']
        if not hasattr(self, 'removed_widget_dictionary'):
            self.removed_widget_dictionary = {}
        widget_number = self.getWidgetNumber(name)
        qwidget = self.getWidget(name, role='field') # retrieves the widget from its name
        if f'{name}_label' in self.getWidgets().keys():
            qlabel = self.getWidget(name, role='label') 
            self.populate_widget_dictionary(self.removed_widget_dictionary, name, qwidget, qlabel)
        else:
            self.populate_widget_dictionary(self.removed_widget_dictionary, name, qwidget)
        formLayout.removeRow(qwidget)                # removes the whole row from the layout
        self.decreaseNumWidgets()                   # updates total number of widgets
        self.remove_widget_from_dictionary(self.getWidgets(), name)
        self.num_removed_widgets += 1
        self.pop_widget_number_dictionary(name, widget_number)



    def getWidget(self, name, role='field'):
        '''returns the Widget by the name with which it has been added

        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label

        Raises ValueError if the role is not field or label.
        '''
        allowed_roles = 'field', 'label'
        if role in allowed_roles:
            return self.widgets[f'{name}_{role}']
        raise ValueError(f'Unexpected role: expected any of {allowed_roles}, got {role}')

    def getWidgetNumber(self, name):
        '''Returns the Widget number by the name with which it has been added.'''
        return self.widget_number_dictionary[name]

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
        '''returns a dictionary of all the widgets in the form'''
        return self.widgets

    def addTitle(self, qlabel, name):
        if isinstance(qlabel, str):
            txt = qlabel
            qlabel = QtWidgets.QLabel(self.uiElements['groupBox'])
            qlabel.setText(txt)
        qlabel.setStyleSheet("font-weight: bold")
        self._addWidget(name, qlabel)

    def addSeparator(self, name):
        # Adds horizontal separator to the form
        frame = QtWidgets.QFrame()
        frame.setFrameShape(QtWidgets.QFrame.HLine)
        frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self._addWidget(name, frame)

    def populate_default_widget_states_dictionary(self, name):
        '''
        Creates an attribute dictionary of default widget states. The entries are in the
        format: {'value': str | bool | int, 'enabled': bool, 'visible': bool}.
        This can be used to restore the default states of the widgets invoking `applyWidgetStates`.
        '''
        if not hasattr(self, 'default_widget_states'):
            self.default_widget_states = {}
        # add the default state of the qwidget
        self.default_widget_states[f'{name}_field'] = self.getWidgetState(name, 'field')
        # add the default state of the qlabel
        if f'{name}_label' in self.widgets.keys():
            self.default_widget_states[f'{name}_label'] = self.getWidgetState(name, 'label')
    
    def set_default_widget_states_visible_true(self):
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
          Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool},
                   ...},
          e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True},
                 'widget2': {'value': 2, 'enabled': False, 'visible': False}}.
        '''
        all_widget_states = {}
        for name, widget in self.widgets.items():
            widget_state = self.getWidgetState(widget)
            all_widget_states[name] = widget_state
        return all_widget_states

    def getWidgetState(self, widget, role=None):
        '''
        Parameters
        ----------
        widget: QWidget or str
            The (name of) widget to get the state of.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to (only if `widget` is a `str`).
            If unspecified, the widget is chosen based on `name=widget`.

        Returns
        -------
        state: dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool},
            e.g. {'value': 1, 'enabled': True, 'visible': True}.
            This can be used to restore the state of the widget using `setWidgetState()`.
        '''
        if widget is None:
            raise ValueError('The widget (or name of widget) must be given')

        if isinstance(widget, str):
            if role is not None:
                if role not in ['label', 'field']:
                    raise ValueError('role must be either "label", "field" or None')
                name = widget + '_' + role
            else:
                name = widget

            try:
                widget = self.widgets[name]
            except KeyError:
                if role is None:
                    try:
                        widget = self.widgets[name + '_field']
                    except KeyError:
                        raise KeyError('No widget with name: ' + name + ' or ' + name + '_field')
                else:
                    raise KeyError('No widget with name: ' + name)

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

        return widget_state

    def applyWidgetState(self, name, state, role=None):
        '''
        Applies the given `state` to the widget with the given `name`.

        Parameters
        ----------
        name: str
            The name of the widget to apply the state to.
        role: str, optional, default None, values: 'label', 'field', None.
            The role of the widget to apply the state to (only if `widget` is a `str`).
            If unspecified, the widget is chosen based on `name`.
        state: dict
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool},
            e.g. {'value': 1, 'enabled': True, 'visible': True}.
        '''
        if role is not None:
            if role not in ['label', 'field']:
                raise ValueError('role must be either "label", "field" or None')
            name = name + '_' + role

        try:
            widget = self.widgets[name]
        except KeyError:
            if role is None:
                try:
                    widget = self.widgets[name + '_field']
                except KeyError:
                    raise KeyError('No widget with name: ' + name + ' or ' + name + '_field')
            else:
                raise KeyError('No widget with name: ' + name)

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
        for name, widget_state in state.items():
            self.applyWidgetState(name, widget_state)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.widget_states = self.getAllWidgetStates()

    def restoreAllSavedWidgetStates(self):
        '''
        All widgets in the form are restored to the saved states. There are saved states only if
        `saveAllWidgetStates` was previously invoked. If there are no previously saved states,
        `default_widget_states` are used instead, after being made visible.
        '''
        if not hasattr(self, 'widget_states'):
            self.set_default_widget_states_visible_true()
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
        self.widget().addWidget(qwidget, qlabel, name)

    def addSpanningWidget(self, qwidget, name):
        self.widget().addSpanningWidget(qwidget, name)

    def insertWidgetToFormLayout(self, row, name, qwidget, qlabel=None):
        '''Invokes `insertWidgetToFormLayout` in `UIFormWidget`.'''
        self.widget().insertWidgetToFormLayout(row, name, qwidget, qlabel)

    def removeWidget(self, name):
        '''
        Removes a widget (and its label if present) from the layout.
        Decreases the counter for the number of widgets in the layout.
        Deletes the field (and label) from the dictionary.
        '''
        self.widget().removeWidget(name)

    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.widget().getNumWidgets()

    def getWidget(self, name, role='field'):
        '''returns the Widget by the name with which it has been added

        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label

        Raises ValueError if the role is not field or label.
        '''
        return self.widget().getWidget(name, role)

    def getWidgets(self):
        '''returns a dictionary of all the widgets in the form'''
        return self.widget().getWidgets()

    def setWidgetVisible(self, name, visible):
        '''Sets the visibility of the widget and associated label with the given name.'''
        self.widget().setWidgetVisible(name, visible)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.widget().saveAllWidgetStates()

    def restoreAllSavedWidgetStates(self):
        '''
        Restore all widgets in the form to the state saved by `saveAllWidgetStates()`.
        If `saveAllWidgetStates()` method was not previously invoked, do nothing.
        '''
        self.widget().restoreAllSavedWidgetStates()

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
        return self.widget().getAllWidgetStates()

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
        return self.widget().getWidgetState(widget, role)

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
        return self.widget().applyWidgetState(name, state, role)

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
        return self.widget().applyWidgetStates(state)


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
