from eqt.ui import FormDialog
from PySide2.QtWidgets import (QCheckBox, QComboBox, QFileDialog, QLabel, QLineEdit, QPushButton, QMessageBox)
from PySide2 import QtWidgets
import os


class SaveSessionDialog(FormDialog):
    def __init__(self, parent=None, title="Save Session"):
        '''
        A dialog to save a session. Prompts the user for a name for the session, and whether to compress the files.

        Parameters
        ----------
        parent : QWidget
            The parent widget.
        title : str
            The title of the dialog.
        '''

        FormDialog.__init__(self, parent, title)
        self.parent = parent
        
        qlabel = QLabel(self.groupBox)
        qlabel.setText("Save session as:")
        qwidget = QLineEdit(self.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        self.addWidget(qwidget, qlabel, 'session_name')

        qwidget = QCheckBox(self.groupBox)
        qwidget.setText("Compress Files")
        qwidget.setEnabled(True)
        qwidget.setChecked(False)
        self.addSpanningWidget(qwidget, 'compress')

        self.Ok.setText('Save')


class SessionDirectorySelectionDialog(FormDialog):
    def __init__(self, parent=None, app_name=None):
        '''
        A dialog to select a directory in which to save and retrieve sessions.

        Parameters
        ----------
        parent : QWidget
            The parent widget.
        app_name : str
            The name of the application.

        Attributes
        ----------
        selected_dir : str
            The selected directory, to be used as the directory in which all sessions are saved.
        '''
        FormDialog.__init__(self, parent, "Select Session Directory")
        self.parent = parent

        self.app_name = app_name

        if app_name is None:
            label_text = 'Select a session directory to save and retrieve all Sessions:'

        else:
            label_text =f'Select a session directory to save and retrieve all {app_name} Sessions:'

        self.addSpanningWidget(QLabel(label_text), 'select_session_directory')


        self.addSpanningWidget(QLabel('No directory selected'), 'selected_dir')

        browse_button = QPushButton('Browse')
        browse_button.clicked.connect(self.browse_for_dir)
        self.addSpanningWidget(browse_button, 'browse_button')

        self.selected_dir = None

        self.Ok.setText('OK')
        self.Cancel.setEnabled(False)

    def browse_for_dir(self):
        dialog = QFileDialog(self.groupBox)
        directory = dialog.getExistingDirectory(self, "Select Directory to Save Sessions")
        self.getWidget('selected_dir').setText(os.path.basename(directory))
        self.selected_dir = directory



class LoadSessionDialog(FormDialog):
    def __init__(self, parent=None, title="Load a Session", location_of_session_files="."):
        '''
        A dialog to load a session. Prompts the user to select a session from a list of available sessions.

        Parameters
        ----------
        parent : QWidget
            The parent widget.
        title : str
            The title of the dialog.
        location_of_session_files : str
            The directory in which to look for session files.
        '''
        FormDialog.__init__(self, parent, title)
        self.parent = parent

        select_dir_button = QPushButton('Select Directory for Loading Sessions') 
        self.buttonBox.addButton(select_dir_button,  QtWidgets.QDialogButtonBox.ActionRole)
        self.Select = select_dir_button

        self.addSpanningWidget(QLabel('Load a Session'), 'load_title')

        location_of_session_files = os.path.abspath(location_of_session_files)

        self.addSpanningWidget(QLabel(f'Currently loading sessions from: {location_of_session_files}'), 'sessions_directory')

        combo = QComboBox(self.groupBox)
        self.addWidget(combo, 'Select a session:', 'select_session')

        self.Ok.setText('Load')
        self.Cancel.setText('New Session')

class WarningDialog(QMessageBox):
    def __init__(self, parent=None, message=None, window_title=None, detailed_text=None):
        '''
        A dialog to display a warning message.
        
        Parameters
        ----------
        parent : QWidget
            The parent widget.
        message : str
            The message to display.
        window_title : str
            The title of the dialog.
        detailed_text : str
            The detailed text to display.
        '''
        QMessageBox.__init__(self, parent)
        self.setIcon(QMessageBox.Information)
        self.setText(message)
        self.setWindowTitle(window_title)
        self.setDetailedText(detailed_text)

class ErrorDialog(QMessageBox):
    def __init__(self, parent=None, message=None, window_title=None, detailed_text=None):
        '''
        A dialog to display an error message.
        The icon is a red circle with a white X.
        
        Parameters
        ----------
        parent : QWidget
            The parent widget.
        message : str
            The message to display.
        window_title : str
            The title of the dialog.
        detailed_text : str
            The detailed text to display.
        '''
        QMessageBox.__init__(self, parent)
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.setWindowTitle(window_title)
        self.setDetailedText(detailed_text)


class AppSettingsDialog(FormDialog):

    def __init__(self, parent=None):
        super(AppSettingsDialog, self).__init__(parent)
        self.setWindowTitle("App Settings")
        dark_checkbox = QCheckBox("Dark Mode")
        self.addSpanningWidget(dark_checkbox, 'dark_checkbox')
        self.Ok.setText("Save")