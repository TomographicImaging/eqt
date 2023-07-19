import sys

from PySide2 import QtWidgets
from PySide2.QtWidgets import QApplication

from eqt import __version__
from eqt.ui.MainWindowWithSessionManagement import MainWindowWithSessionManagement
from eqt.ui.UIFormWidget import FormWidget
from eqt.ui.UISliderWidget import UISliderWidget


class ExampleMainWindowWithSessionManagement(MainWindowWithSessionManagement):
    '''
    This is an example of a MainWindowWithSessionManagement.
    It is used to show how to use the MainWindowWithSessionManagement class.

    To test out this example, change the state of the widgets and save the session.
    Then load the session again and check if the state of the widgets is the same as before.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        form_widget = FormWidget(self)
        add_every_widget_to_form(form_widget)
        self.setCentralWidget(form_widget)
        self.addToMenu()

    def addToMenu(self):
        ''' Adds an example extra menu.'''
        extra_menu = self.menu_bar.addMenu("Extra Menu")
        self.menu_bar.addMenu(extra_menu)
        self.menus["Extra"] = extra_menu

    def getSessionConfig(self):
        '''
        This function is called when the user wants to save the current session.
        We need to add the state of the widgets to the config.

        Returns
        -------
        config : dict
            The config of the current session.
        '''

        form_widget = self.centralWidget()
        all_widget_states = form_widget.getAllWidgetStates()

        config = {'form_widget': all_widget_states}

        return config

    def finishLoadConfig(self, process_name):
        '''
        This function is called after the config of the chosen session is loaded.
        It is used to set the state of the widgets.
        '''
        form_widget_config = self.config['form_widget']
        form_widget = self.centralWidget()
        form_widget.applyWidgetStates(form_widget_config)
        super().finishLoadConfig(process_name)


def add_every_widget_to_form(form):
    '''
    Generate every widget and add it to the form

    Parameters
    ----------
    form : FormWidget, FormDialog or FormDockWidget
        The form to add the widgets to
    '''
    form.addWidget(QtWidgets.QLabel('test label'), 'Label: ', 'label')
    form.addWidget(QtWidgets.QCheckBox('test checkbox'), 'CheckBox: ', 'checkBox')
    form.addWidget(QtWidgets.QComboBox(), 'ComboBox: ', 'comboBox')
    form.addWidget(QtWidgets.QDoubleSpinBox(), 'DoubleSpinBox: ', 'doubleSpinBox')
    form.addWidget(QtWidgets.QSpinBox(), 'SpinBox: ', 'spinBox')
    form.addWidget(QtWidgets.QSlider(), 'Slider: ', 'slider')
    form.addWidget(UISliderWidget(QtWidgets.QLabel()), 'UISliderWidget: ', 'uiSliderWidget')
    form.addWidget(QtWidgets.QRadioButton('test'), 'RadioButton: ', 'radioButton')
    form.addWidget(QtWidgets.QTextEdit('test'), 'TextEdit: ', 'textEdit')
    form.addWidget(QtWidgets.QPlainTextEdit('test'), 'PlainTextEdit: ', 'plainTextEdit')
    form.addWidget(QtWidgets.QLineEdit('test'), 'LineEdit: ', 'lineEdit')
    form.addWidget(QtWidgets.QPushButton('test'), 'Button: ', 'button')


def create_main_window():
    window = ExampleMainWindowWithSessionManagement(f"Example Session Main Window{__version__}",
                                                    "Example0", settings_name="Example0")

    return window


def main():
    # open main window:
    app = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
