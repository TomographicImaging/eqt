from PySide2 import QtWidgets


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
