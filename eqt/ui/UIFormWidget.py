# Author: Edoardo Pasca, Laura Murgatroyd, Samuel Stock

from PySide2 import QtWidgets
from eqt.ui.UISliderWidget import UISliderWidget


class UIFormWidget(object):
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

        self.num_widgets = 0
        self.uiElements = {
            'verticalLayout': verticalLayout,
            'groupBox': groupBox,
            'groupBoxFormLayout': groupBoxFormLayout}
        self.widgets = {}

    @property
    def groupBox(self):
        return self.uiElements['groupBox']

    def addSpanningWidget(self, qwidget, name):
        self._addWidget(name, qwidget)

    def addWidget(self, qwidget, qlabel, name):
        self._addWidget(name, qwidget, qlabel)

    def getWidget(self, name, role='field'):
        '''returns the Widget by the name with which it has been added
        
        By default it returns the widget that is the field in the form. 
        The user can get the label by specifying the role to be label
        
        Raises ValueError if the role is not field or label.
        '''
        allowed_roles = ['field', 'label']
        if role in allowed_roles:
            return self.widgets['{}_{}'.format(name, role)]
        raise ValueError('Unexpected role: expected any of {}, got {}'.format(allowed_roles, role))

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
            except:
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

    def _addWidget(self, name, qwidget, qlabel=None):
        formLayout = self.uiElements['groupBoxFormLayout']

        # Create the widgets:

        widgetno = self.num_widgets

        # add the field
        field = '{}_field'.format(name)
        self.widgets[field] = qwidget

        if qlabel is not None:
            # add the label
            label = '{}_label'.format(name)
            if isinstance(qlabel, str):
                txt = qlabel
                qlabel = QtWidgets.QLabel(self.uiElements['groupBox'])
                qlabel.setText(txt)
            formLayout.setWidget(
                widgetno, QtWidgets.QFormLayout.LabelRole, qlabel)

            # save a reference to label widgets in the dictionary
            self.widgets[label] = qlabel

            field_form_role = QtWidgets.QFormLayout.FieldRole

        else:
            # In the case we don't have a qlabel, set a spanning widget:
            field_form_role = QtWidgets.QFormLayout.SpanningRole

        formLayout.setWidget(widgetno, field_form_role, qwidget)
        self.num_widgets += 1


    def getAllWidgetStates(self):
        '''
        Returns the state of all widgets in the form.
        Returns
        -------
        dict
            A dictionary of the states of all widgets in the form, keyed by the name of the widget, 
            and the value being a dictionary with the state of the widget. The dictionary
            containing the state of the widget has the keys 'visible', 'value' and 'enabled', and the values

        '''
        all_widget_states = {}
        for name, widget in self.widgets.items():
            widget_state = self.getWidgetState(widget)
            all_widget_states[name] = widget_state
        return all_widget_states

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
        Applies the given state to the widgets in the form.

        Parameters
        ----------
        state: dict
            A dictionary of the state of the widgets, with the key being the name of the widget, and the value
            being a dictionary with the keys 'value', 'enabled', and 'visible', which store the value, enabled state,
            and visible state of the widget.
            The value may be a string, boolean, or integer, depending on the type of widget.
            E.g. {{'widget1': {'value': 1, 'enabled': True, 'visible': True}, 'widget2': {'value': 2, 'enabled': False, 'visible': False}}
        '''
        for name, widget_state in state.items():
            self.applyWidgetState(name, widget_state)

    def saveAllWidgetStates(self):
        '''
        Saves the state of all widgets in the form.
        This can be used to restore the state of the widgets using the restoreAllSavedWidgetStates method.
        '''
        self.widget_states = self.getAllWidgetStates()
    
    def restoreAllSavedWidgetStates(self):
        '''
        Restores the state of all widgets in the form to the state saved by the saveAllWidgetStates method.
        If the saveAllWidgetStates method has not been called, this method will do nothing.
        '''
        if hasattr(self, 'widget_states'):
            self.applyWidgetStates(self.widget_states)

class FormWidget(QtWidgets.QWidget, UIFormWidget):
    def __init__(self, parent=None):
        # dockWidgetContents = QtWidgets.QWidget()

        QtWidgets.QWidget.__init__(self, parent)
        self.createForm()


class FormDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None, title=None):
        QtWidgets.QDockWidget.__init__(self, parent)
        widget = FormWidget(parent)
        self.setWidget(widget)
        if title is not None:
            self.setObjectName(title)

    def addWidget(self, qwidget, qlabel, name):
        self.widget().addWidget(qwidget, qlabel, name)

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
        Saves the state of all widgets in the form.
        This can be used to restore the state of the widgets using the restoreAllSavedWidgetStates method.
        '''
        self.widget().saveAllWidgetStates()

    def restoreAllSavedWidgetStates(self):
        '''
        Restores the state of all widgets in the form to the state saved by the saveAllWidgetStates method.
        If the saveAllWidgetStates method has not been called, this method will do nothing.
        '''
        self.widget().restoreAllSavedWidgetStates()

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
        return self.widget().getAllWidgetStates()

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
        return self.widget().getWidgetState(widget, role)

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
        return self.widget().applyWidgetState(name, state, role)

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
