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
    
    def hide_widgets(self, names):
        formLayout = self.uiElements['groupBoxFormLayout']
        form_widget_names = list(self.widgets.keys())
        names_to_hide = names

        widget_indices = []
        for name in names_to_hide:
            field_name = name + '_field'
            try:
                widget_indices.append(form_widget_names.index(field_name))
            except ValueError:
                print("Warning: Could not find widget with name: ", name)

        # We must save the widgets in the order they appeared in the form so that when they are
        # shown they are in the correct order:
        ordered_names_to_hide = [x for _, x in sorted(zip(widget_indices, names_to_hide))]

        if not hasattr(self, 'hidden_widgets'):
            self.hidden_widgets = {}

        for name in ordered_names_to_hide:
            field_name = name + '_field'
            label_name = name + '_label'
            # all widgets have a field:
            try:
                self.hidden_widgets[field_name] = self.widgets[field_name]
                formLayout.removeWidget(self.widgets[field_name])
                self.widgets[field_name].setVisible(False)
                self.widgets.pop(field_name)
            except KeyError:
                print("Warning: Could not find widget with name: ", field_name)
            # some widgets won't have a label:
            try:
                self.hidden_widgets[label_name] = self.widgets[label_name]
                formLayout.removeWidget(self.widgets[label_name])
                self.widgets.pop(label_name)
            except KeyError:
                pass


    def show_widgets(self, names):
        # We must retrieve the widgets in the order they first appeared in the form so that when they are
        # shown they are in the correct order:
        hidden_widget_names = list(self.hidden_widgets.keys())
        names_to_show = names
        widget_indices = []
        for name in names_to_show:
            field_name = name + '_field'
            try:
                widget_indices.append(hidden_widget_names.index(field_name))
            except ValueError:
                print("Warning: Could not find hidden widget with name: ", field_name)
        ordered_names_to_show = [x for _, x in sorted(zip(widget_indices, names_to_show))]
        for name in ordered_names_to_show:
            field_name = name + '_field'
            label_name = name + '_label'
            if field_name in hidden_widget_names:
                if label_name in hidden_widget_names:
                    self.addWidget(self.hidden_widgets[field_name], self.hidden_widgets[label_name], name)
                    self.hidden_widgets[field_name].setVisible(True)
                    self.hidden_widgets[field_name].setVisible(True)
                    self.hidden_widgets.pop(label_name)
                else:
                    self.addSpanningWidget(self.hidden_widgets[field_name], name)
                self.hidden_widgets.pop(field_name)
            else:
                print("Warning: Could not find widget with name: ", field_name)



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


class UIFormFactory(QtWidgets.QWidget):
    # def generateUIFormView(QtWidgets.QWidget):
    '''creates a widget with a form layout group to add things to

    basically you can add widget to the returned groupBoxFormLayout and paramsGroupBox
    The returned dockWidget must be added with
    main_window.addDockWidget(QtCore.Qt.RightDockWidgetArea, dockWidget)
    '''
    @staticmethod
    def getQDockWidget(parent=None):
        return FormDockWidget(parent)

    @staticmethod
    def getQWidget(parent=None):
        return FormWidget(parent)
