import json
import os
import shutil
import sys
import tempfile
import zipfile
from datetime import datetime
from functools import partial

import qdarkstyle
from eqt.threading import Worker
from eqt.ui import FormDialog, UIFormFactory, UIMultiStepFactory
from eqt.ui.UIMultiStepWidget import MultiStepWidget
from eqt.ui.UIStackedWidget import StackedWidgetFactory
from PySide2 import QtCore
from PySide2.QtCore import QProcess, QRegExp, QSettings, Qt, QThreadPool
from PySide2.QtGui import QCloseEvent, QKeySequence, QRegExpValidator
from PySide2.QtWidgets import (QAction, QApplication, QCheckBox, QComboBox,
                               QDialog, QDialogButtonBox, QDockWidget,
                               QDoubleSpinBox, QFileDialog, QFormLayout,
                               QFrame, QGroupBox, QHBoxLayout, QLabel,
                               QLineEdit, QMainWindow, QMenu, QMessageBox,
                               QProgressDialog, QPushButton, QSlider, QSpinBox,
                               QStackedWidget, QTabWidget)
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

# TODO: fix progress of zipping files


class MainWindow(QMainWindow):
    ''''
    A MainWindow with:
    - File menu including settings dialog to set stylesheet
    - methods to create + update progress bar in a dialog window
    - method for warning dialog
    - method to start qprocess and attach connections to it
    - Methods to save session and produce save dialogs (optionally)
    '''

    def __init__(self, title="", save_sessions=True, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        ''''
        if save_sessions is set to True:
        - a folder will be created for the session
        - 'Save' and 'Save & Exit' buttons will be added to the File menu
        - Upon closing the app user will be prompted whether to save
        - Save dialog has option to compress files'''

        self.save_sessions = save_sessions

        self.threadpool = QThreadPool()

        self.setWindowTitle(title)
        #self.create_dockwidgets()

        print("The title is: ", title)

        self.settings = QSettings(title)

        self.set_app_style()

        self.create_menu()

        self.setTabPosition(QtCore.Qt.AllDockWidgetAreas, QTabWidget.North)

        if self.save_sessions:
            self.config = {} # config for saving session
            self.create_session_folder(title)

    
    def set_app_style(self):
        '''Sets app stylesheet, based on user's settings '''
        if self.settings.value("dark_mode") is None:
            self.settings.setValue("dark_mode", "true")
        if self.settings.value("dark_mode") == "true":
            palette=DarkPalette
        else:
            palette=LightPalette
        style = qdarkstyle.load_stylesheet(palette=palette)
        print("setting style to: ", palette)
        self.setStyleSheet(style)

    def create_menu(self):
        ''' creates menu '''
        self.menu = self.menuBar()

        file_menu = QMenu("File")
        self.file_menu = file_menu

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        file_menu.addAction(settings_action)

        if self.save_sessions:
            save_action = QAction("Save", self)
            save_action.triggered.connect(partial(self.CreateSaveWindow, event="SaveEvent"))
            file_menu.addAction(save_action)

            save_exit_action = QAction("Save & Exit", self)
            save_exit_action.triggered.connect(partial(self.CreateSaveWindow, event=QCloseEvent))
            file_menu.addAction(save_exit_action)


        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.menu.addMenu(file_menu)

    # dialogs: --------------------------------------------------------------------------

    def warningDialog(self, message='', window_title='', detailed_text=''):
        ''' Produces a warning dialog with:
        window_title (str): title of the window
        message (str): error message in the window
        detailed_text (str): message which appears when window is expanded'''
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Information)
        dialog.setText(message)
        dialog.setWindowTitle(window_title)
        dialog.setDetailedText(detailed_text)
        dialog.setStandardButtons(QMessageBox.Ok)
        retval = dialog.exec_()
        return retval

    def create_progress_window(self, title, text, max = 100, cancel = None):
        ''' Creates a dialog box with a progress bar.
        title (str): title of the window
        text (str): text which appears above progress bar
        max (int): maximum value of the progress bar
        cancel (method): method to carry out if progress bar is cancelled. If set to None, no cancel
        button is added to the dialog, so it is impossible to cancel the task'''
        # move to eqt MainWindow
        self.progress_window = QProgressDialog(text, "Cancel", 0, max, self, QtCore.Qt.Window) 
        self.progress_window.setWindowTitle(title)
        #self.progress_window.setWindowModality(QtCore.Qt.ApplicationModal) #This means the other windows can't be used while this is open
        self.progress_window.setMinimumDuration(0.01)
        self.progress_window.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, True)
        self.progress_window.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.progress_window.setAutoClose(True)
        if cancel is None:
            self.progress_window.setCancelButton(None)
        else:
            self.progress_window.canceled.connect(cancel)

    def update_progress_bar(self, value):
        ''' updates the progress bar in the progress dialog
        if value (float/int) is bigger than the current progress value'''
        if int(value) > self.progress_window.value():
            self.progress_window.setValue(value)


    ## Settings dialog --------------------------------------------------------------------

    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        self.setup_settings_dialog(settings_dialog)
        settings_dialog.show()

    def setup_settings_dialog(self, settings_dialog):
        settings_dialog.Ok.connect(lambda: self.settings_dialog_accept(settings_dialog))
        settings_dialog.Cancel.connect(lambda: self.settings_dialog_quit(settings_dialog))

        if self.settings.value("dark_mode") is not None:
            if self.settings.value("dark_mode") == "true":
                settings_dialog.fw.widgets['dark_checkbox_field'].setChecked(True)
            else:
                settings_dialog.fw.widgets['dark_checkbox_field'].setChecked(False)
        else:
            settings_dialog.fw.widgets['dark_checkbox_field'].setChecked(True)
    
    
    def settings_dialog_accept(self, settings_dialog):
        print("qt settings dialog accept")
        if settings_dialog.fw.widgets['dark_checkbox_field'].isChecked():
            self.settings.setValue("dark_mode", "true")
        else:
            self.settings.setValue("dark_mode", "false")
        self.set_app_style()
            
        settings_dialog.close()

    def settings_dialog_quit(self, settings_dialog):
        settings_dialog.close()

    ### QProcess -------------------------------------------------------------------------------------------

    def start_qprocess(self, command, process_name, finish_connection=None,  error_connection=None):
        ''' start a QProcess with:
        command = command to be run
        process_name = str name of process
        finish_connection = method to be run when command is completed
        error_connection = event to occur in case of error, by default an error dialog is produced'''
        self.create_progress_window("Running {}".format(process_name), 
                "{}".format(command), 100)
        process = QProcess()
        self.process_failed = False
        if finish_connection is not None:
            process.finished.connect(lambda: self.qprocess_finish_connection(finish_connection))
        if error_connection is not None:
            process.errorOccurred.connect(error_connection)
        else:
            process.errorOccurred.connect(partial(self.update_progress_error, process, process_name))
        process.readyReadStandardOutput.connect(lambda: self.update_qprocess_progress(process))
        process.readyReadStandardError.connect(lambda: self.update_progress_error(process, process_name))
        process.start(command)

    def update_qprocess_progress(self, process):
        while(process.canReadLine()):
            string = process.readLine()  
            line = str(string, "utf-8")
            
            if hasattr(self, 'progress_window'):
                self.progress_window.setLabelText(line)
            sys.stdout.flush()


    def update_progress_error(self, process, process_name, error=None):
        error_message = process.readAllStandardError()
        if error_message is not None:
            string = error_message
            line = str(string, "utf-8")
        else:
            line = str(error) + process.errorString()

        if not "Warning" in line:
            self.process_failed = True
            
            if hasattr(self, 'progress_window'):
                self.progress_window.close()
            process.kill()
            self.warningDialog(message="An error occurred with: {}".format(process_name), window_title=process_name, detailed_text=line)
            
            sys.stdout.flush()

    def qprocess_finish_connection(self, connection):
        self.progress_window.close()
        if not self.process_failed:
            connection()


    # Dealing with saving sessions: --------------------------------------------------------

    def create_session_folder(self, title):
        date_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        prefix = '{}-{}-'.format(title, date_time)
        self.session_folder = tempfile.mkdtemp(prefix=prefix, dir='.')
        os.chdir(self.session_folder)

    def CreateSaveWindow(self, event):
        self.should_really_close = False
        dialog = SaveDialog(parent=self, title='Save Session', event=event)
        self.SaveWindow = dialog


    def closeEvent(self, event):
        if self.save_sessions:
            if not hasattr(self, 'should_really_close') or not self.should_really_close:
                self.CreateSaveWindow(QCloseEvent)
            self.threadpool.waitForDone()
            if not hasattr(self, 'should_really_close') or not self.should_really_close:
                event.ignore()
            else:
                event.accept()
        else:
            event.accept()

    def create_session_config(self):
        self.config = {}
        now = datetime.now()
        now_string = now.strftime("%d-%m-%Y-%H-%M")
        self.config['datetime'] = now_string


    def save_session(self, session_name, compress, event):
        ''' 
        session_name = str - name to give session folder
        compress = bool - whether to compress session zip folder
        event = event causing session to be saved. If QCloseEvent type,
        then app is closed after session is saved, otherwise app remains
        open.
        Saves self.config to a json file.
        Moves contents of session folder to a zipfolder with name given by 
        session_name and the date and time, which is
        optionally compressed.'''
        suffix_text = "_" + session_name + "_" + self.config['datetime']

        os.chdir('..')
        tempdir = shutil.move(self.session_folder, suffix_text)

        self.session_folder = suffix_text

        fd, f = tempfile.mkstemp(suffix=suffix_text + ".json", dir = tempdir) #could not delete this using rmtree?

        with open(f, "w+") as tmp:
            json.dump(self.config, tmp)

        os.close(fd)

        self.create_progress_window("Saving", "Saving Session")
  
        zip_worker = Worker(self.ZipDirectory, self.session_folder, compress)
        if type(event) == QCloseEvent:
            zip_worker.signals.finished.connect(lambda: self.delete_session_folder(event))
        else:
            zip_worker.signals.finished.connect(self.CloseSaveWindow)
        zip_worker.signals.progress.connect(self.update_progress_bar)
        self.threadpool.start(zip_worker)
    
    def CloseSaveWindow(self):
        # TODO: rename /document
        # move back to session dir in case we moved
        # out of it for zipping etc.:
        os.chdir(self.session_folder)
        if hasattr(self, 'progress_window'):
            self.progress_window.setValue(100)
        self.SaveWindow.close()
        self.should_really_close = True
       
    def ZipDirectory(self, *args, **kwargs):
        # move to eqt MainWindow
        directory, compress = args
        progress_callback = kwargs.get('progress_callback', None)

        zip = zipfile.ZipFile(directory + '.zip', 'a')

        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)

        if compress:
            compress_type = zipfile.ZIP_DEFLATED
        else:
            compress_type = zipfile.ZIP_STORED

        for r, d, f in os.walk(directory):
            for _file in f:
                fname = os.path.join(r, _file)
                arcname = fname[len(directory)+1:] #TODO: do we need this?
                zip.write(fname, arcname, compress_type=compress_type)
                progress_callback.emit(os.path.getsize(fname)/total_size)
        zip.close()


    def delete_session_folder(self, event):
        ''' Delete the session folder '''
        if hasattr(self, 'progress_window'):
            self.progress_window.setLabelText("Closing")
            self.progress_window.setMaximum(100)
            self.progress_window.setValue(98)
        try:
            shutil.rmtree(self.session_folder)
        except FileNotFoundError:
            os.chdir('..')
            shutil.rmtree(self.session_folder)

        if hasattr(self, 'progress_window'):
            self.progress_window.setValue(100)
        if hasattr(self, 'SaveWindow'):
            self.SaveWindow.close()

        if event != "new session":
            self.close()



# TODO: move connections outside of this class

class SaveDialog(FormDialog):
    def __init__(self, parent=None, title="Save Session", event=None):
        FormDialog.__init__(self, parent, title)
        self.parent = parent
        self.Ok.setText('Save')
        # add input 1 as QLineEdit
        qlabel = QLabel(self.groupBox)
        qlabel.setText("Save session as:")
        qwidget = QLineEdit(self.groupBox)
        qwidget.setClearButtonEnabled(True)
        rx = QRegExp("[A-Za-z0-9]+")
        validator = QRegExpValidator(rx, self) #need to check this
        qwidget.setValidator(validator)
        # finally add to the form widget
        self.addWidget(qwidget, qlabel, 'session_name')
        
        qwidget = QCheckBox(self.groupBox)
        qwidget.setText("Compress Files")
        qwidget.setEnabled(True)
        qwidget.setChecked(False)
        self.addSpanningWidget(qwidget,'compress')
        
        self.save_button = QPushButton("Save")
        # We have 2 instances of the window.
        if event ==  QCloseEvent: # m
            # This is the case where we are quitting the app and the window asks if we
            # would like to save
            self.Cancel.clicked.connect(lambda: self.just_quit())
            self.Ok.clicked.connect(lambda: self.save_quit_accepted())
            self.Cancel.setText('Quit without saving')
        else:
            # This is the case where we are just choosing to 'Save' in the file menu
            # so we never quit the app.
            self.Cancel.clicked.connect(lambda: self.save_quit_rejected())
            self.Ok.clicked.connect(lambda: self.save_accepted())
            self.Cancel.setText('Cancel')
        
        self.exec()

    def save_accepted(self):
        self.parent.should_really_close = False
        compress = self.widgets['compress_field'].isChecked()
        self.close()
        self.parent.save_session(self.widgets['session_name_field'].text(), compress, None)


    def save_quit_accepted(self):
        #Load Saved Session
        self.parent.should_really_close = True
        compress = self.widgets['compress_field'].isChecked()
        self.close()
        self.parent.save_session(self.widgets['session_name_field'].text(), compress, QCloseEvent())
        

    def just_quit(self):
        event = QCloseEvent()
        self.close()
        self.parent.delete_session_folder(event) # remove tempdir for this session.
        self.parent.should_really_close = True
        self.close()

    def save_quit_rejected(self):
        self.parent.should_really_close = False
        self.close()



class SettingsDialog(QDialog):

    def __init__(self, parent):
        super(SettingsDialog, self).__init__(parent)

        self.parent = parent

        self.setWindowTitle("Settings")

        fw = UIFormFactory.getQWidget(parent=self)

        dark_checkbox = QCheckBox("Dark Mode")

        fw.addSpanningWidget(dark_checkbox, 'dark_checkbox')

        self.buttonBox = QDialogButtonBox(
           QDialogButtonBox.Save | QDialogButtonBox.Cancel,
           Qt.Horizontal, self)
        fw.uiElements['verticalLayout'].addWidget(self.buttonBox)
        self.setLayout(fw.uiElements['verticalLayout'])

        self.fw = fw

    @property
    def Ok(self):
        '''returns a reference to the Dialog Ok button to connect its signals'''
        return self.buttonBox.accepted
    @property
    def Cancel(self):
        '''returns a reference to the Dialog Cancel button to connect its signals'''
        return self.buttonBox.rejected



def create_main_window():
    window = MainWindow("Test Main Window")
    return window


def main():
    app = QApplication(sys.argv)
    window = create_main_window()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
