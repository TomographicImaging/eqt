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
        self.widget_number_dictionary = {}
        self.uiElements = {
            'verticalLayout': verticalLayout, 'groupBox': groupBox,
            'groupBoxFormLayout': groupBoxFormLayout}
        self.widgets = {}
        self.default_widgets = {}

    @property
    def num_widgets(self):
        return self.uiElements['groupBoxFormLayout'].rowCount()

    @property
    def groupBox(self):
        return self.uiElements['groupBox']

    def insertWidgetToFormLayout(self, row, name, qwidget, qlabel=None):
        '''
        Inserts a widget and a label widget , or a spanning widget if 'qlabel' is None, to the form layout
        in the position specified by row. If row is out of bounds, the widget is added at the end. 
        If 'name' is already in use, it raises an error.
        It adds to the widget dictionary and the default states dictionary.

        Parameters:
        ----------
        row: int
        name: str
        qwidget: qwidget
        qlabel: qlabel widget or str
        '''
        
        if f'{name}_field' in self.widgets.keys():
            raise ValueError(f'The name of widget you are trying to insert, {name}, is used already. Choose another name.')

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
        self._addToWidgetNumberDictionary(name, row)
        self._addToWidgetDictionary(self.default_widgets, name, qwidget, qlabel)
        self.addToDefaultWidgetStatesDictionary(name)

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

    def _addToWidgetDictionary(self, dictionary, name, qwidget, qlabel = None):
        '''Adds the field (and label if present) in the widget dictionary.'''
        dictionary[f'{name}_field'] = qwidget
        if qlabel is not None:
            dictionary[f'{name}_label'] = qlabel
        
    def _addToWidgetNumberDictionary(self, name, widget_number): 
        '''
        Adds one item in the widget-number dictionary whose key is name and value is 
        the current widget number (i.e. row) in the form layout.
        As one widget is inserted, the widget numbers associated to the other widgets 
        in the layout are updated.

        Parameters:
        ---------------
        name: string
            name of the widget
        widget_number : int
            position of the widget in the form layout, i.e. row, in the current state
        '''
        if widget_number == -1:
            self.widget_number_dictionary[name] = self.num_widgets - 1 
        else:
            for key, value in self.widget_number_dictionary.items():
                if value >= widget_number:
                    self.widget_number_dictionary[key] = value + 1
            self.widget_number_dictionary[name] = widget_number

    def _popWidgetNumberDictionary(self, name, widget_number):
        '''
        Removes one item in the widget-number dictionary whose key is name and value is 
        the widget number (i.e. row) in the form layout.
        As one widget is removed, the widget numbers associated to the other widgets 
        in the layout are updated.

        Parameters:
        ---------------
        name: string
            name of the widget
        widget_number : int
            position of the widget in the form layout, i.e. row, in the current state
        '''
        for key, value in self.widget_number_dictionary.items():
            if value > widget_number:
                self.widget_number_dictionary[key] = value - 1
        self.widget_number_dictionary.pop(name) 

    def _popWidgetFromDictionary(self, dictionary, name):
        '''
        Removes the item(s) associated with `name` from a dictionary.

        Parameters:
        -----------------
        dictionary :  dict
        name: str
            Format: {name}
        '''
        if name in dictionary.keys():
            dictionary.pop(name) 
        if f'{name}_field' in dictionary.keys():
            dictionary.pop(f'{name}_field')      
        if f'{name}_label' in dictionary.keys():
            dictionary.pop(f'{name}_label') 

    def addWidget(self, qwidget, qlabel, name):
        '''Adds a qwidget and a qlabel widget in the same row of the form layout.'''
        self._addWidget(name, qwidget, qlabel)
    
    def addSpanningWidget(self, qwidget, name):
        '''Adds a spanning qwidget occupying the full row in the form layout.'''
        self._addWidget(name, qwidget)
        
    def getNumWidgets(self):
        '''
        Returns the number of widgets in the form.
        '''
        return self.num_widgets

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
        formLayout = self.uiElements['groupBoxFormLayout']
        if not hasattr(self, 'removed_widgets_dictionary'):
            self.removed_widgets_dictionary = {}
        widget_number = self.getWidgetNumber(name)
        qwidget = self.getWidget(name, role='field') 
        if f'{name}_label' in self.getWidgets().keys():
            qlabel = self.getWidget(name, role='label') 
            self._addToWidgetDictionary(self.removed_widgets_dictionary, name, qwidget, qlabel)
            self.getWidget(name, 'label').setParent(None)
        else:
            self._addToWidgetDictionary(self.removed_widgets_dictionary, name, qwidget)
        self.getWidget(name, 'field').setParent(None)  
        formLayout.removeRow(self.widget_number_dictionary[name])   
        self._popWidgetFromDictionary(self.getWidgets(), name) 
        self._popWidgetNumberDictionary(name, widget_number)        

    def getWidget(self, name, role='field'):
        '''Returns the widget by the name with which it has been added

        By default it returns the widget that is the field in the form.
        The user can get the label by specifying the role to be label

        Raises ValueError if the role is not field or label.
        '''
        allowed_roles = 'field', 'label'
        if role in allowed_roles:
            return self.widgets[f'{name}_{role}']
        raise ValueError(f'Unexpected role: expected any of {allowed_roles}, got {role}')

    def getWidgetNumber(self, name):
        '''Returns the widget number by the widget name.'''
        return self.widget_number_dictionary[f'{name}']

    def getWidgetNumberDictionary(self):
        '''Returns the widget number dictionary.'''
        return self.widget_number_dictionary

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
    
    def getRemovedWidgets(self):
        '''Returns the dictionary of the removed widgets previously present in the form.'''
        return self.removed_widgets_dictionary

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

    def addToDefaultWidgetStatesDictionary(self, name):
        '''
        Creates an attribute dictionary of default widget states. The entries are in the
        format: {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number': int}.
        This can be used to restore the default states of the widgets invoking `applyWidgetStates`.
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
          Format: {'widget_name': {'value': str | bool | int, 'enabled': bool, 'visible': bool},
                   ...},
          e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True},
                 'widget2': {'value': 2, 'enabled': False, 'visible': False}}.
        '''
        all_widget_states = {}
        for key, widget in self.widgets.items():
            all_widget_states[key]  = self.getWidgetState(widget)
        return all_widget_states

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
        if widget is None:
            raise ValueError('The widget (or name of widget) must be given')

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
                raise KeyError('No widget associated with the dictionary key `'+ name_role)
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

        widget_state['widget_number'] = self.widget_number_dictionary[name]
        return widget_state

    def _getNameAndRoleFromKey(self, key):
        '''
        Given a key, returns the name and the role. 
        Role can be included as a suffix or is `field` by default.
        
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
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int},
                    e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
        '''
        if role is not None:
            if role in ['label', 'field']:
                name_role = name + '_' + role
            else:
                raise ValueError(f'Role must be either "label", "field" or None. Got {role}.')
        else:
            name_role = f'{name}_field'
        
        #retrieve widget
        try:
            if name_role in self.widgets.keys():
                widget = self.widgets[name_role]
            elif hasattr(self, 'removed_widgets_dictionary'):
                if name_role in self.removed_widgets_dictionary.keys():
                    widget = self.removed_widgets_dictionary[name_role]
        except KeyError:
            raise KeyError('No widget associated with the dictionary key `'+name_role+'`')
        #apply state
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
                elif key == 'widget_number':
                    if value != self.widget_number_dictionary[name]:
                        self.widget_number_dictionary[name] = value

    def applyWidgetStates(self, states):
        '''
        Reorders the states dictionary in ascending widget number.
        Removes the widgets in the form which are not present in the states. 
        If the widgets in the states are not present in the form, 
        they are retrieved from the removed-widgets dictionary and inserted at position 
        given by the widget number recorded in the states. An error is raised when the 
        widget in thet state is not in the form nor in the removed widgets.
        Applies the given states to the form's widgets.

        Parameters
        ----------
        states: nested_dict        Reorders the states dictionary in ascending widget number.
          Format: {'name_field': {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int},
                    'name_label': {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int}, ...},
                  e.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0},
                  'widget2': {'value': 2, 'enabled': False, 'visible': False, 'widget_number' : 1}}.
        '''
        
        # add widgets if necessary
        states = dict(sorted(states.items(), key = lambda tup: (tup[1]['widget_number'])))
        for key, widget_state in states.items():
            name, role = self._getNameAndRoleFromKey(key)
            if key in self.widgets.keys():
                pass
            elif hasattr(self, 'removed_widgets_dictionary'):
                if key in self.removed_widgets_dictionary.keys():
                    if role == 'field':
                        widget_number = states[key]['widget_number']
                        qwidget = self.removed_widgets_dictionary[key]
                        
                        if f'{name}_label' in self.removed_widgets_dictionary.keys():
                            qlabel = self.removed_widgets_dictionary[f'{name}_label']
                            self.insertWidgetToFormLayout(widget_number, name, qwidget, qlabel)
                        else:
                            self.insertWidgetToFormLayout(widget_number, name, qwidget)
            else:
                raise KeyError('No widget associated with the dictionary key `' + key + '`')
            self.applyWidgetState(name, widget_state, role)
        # remove extra widgets
        set_to_remove = set()
        if self.widgets.keys() > states.keys():
            for key in self.widgets.keys():
                if key not in states.keys():
                    name = self._getNameAndRoleFromKey(key)[0]
                    set_to_remove.add(name)
            for el in set_to_remove:
                self.removeWidget(el)


    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets currently present in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.widget_states = self.getAllWidgetStates()

    def getWidgetStates(self):
        '''Returns the saved widget states.'''
        return self.widget_states

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
        '''Adds a qwidget and a qlabel widget in the same row of the form layout.'''
        self.widget().addWidget(qwidget, qlabel, name)

    def addSpanningWidget(self, qwidget, name):
        '''Adds a spanning qwidget occupying the full row in the form layout.'''
        self.widget().addSpanningWidget(qwidget, name)

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

    def getWidgetNumber(self, name):
        '''Returns the widget number by the widget name.'''
        return self.widget().getWidgetNumber(name)

    def getWidgetNumberDictionary(self):
        '''Returns the widget number dictionary.'''
        return self.widget().getWidgetNumberDictionary()

    def getRemovedWidgets(self):
        '''Returns the dictionary of the removed widgets previously present in the form.'''
        return self.widget().getRemovedWidgets()

    def setWidgetVisible(self, name, visible):
        '''Sets the visibility of the widget and associated label with the given name.'''
        self.widget().setWidgetVisible(name, visible)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets currently present in the form.
        To later restore the states, use `restoreAllSavedWidgetStates()`.
        '''
        self.widget().saveAllWidgetStates()

    def getWidgetStates(self):
        '''Returns the saved widget states.'''
        self.widget().getWidgetStates()

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
            Format: {'value': str | bool | int, 'enabled': bool, 'visible': bool, 'widget_number' : int},
                    e.g. {'value': 1, 'enabled': True, 'visible': True, 'widget_number' : 0}.
        '''
        return self.widget().applyWidgetState(name, state, role)

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
