import json
import os
import shutil
from datetime import datetime
from functools import partial
from PySide2.QtGui import QCloseEvent, QKeySequence
from PySide2.QtWidgets import QAction

from eqt.io import zip_directory
from eqt.threading import Worker
from eqt.ui.MainWindowWithProgressDialogs import MainWindowWithProgressDialogs
from eqt.ui.SessionDialogs import (ErrorDialog, LoadSessionDialog,
                                   SaveSessionDialog,
                                   SessionDirectorySelectionDialog)


class MainWindowWithSessionManagement(MainWindowWithProgressDialogs):

    '''
    A base class for a main window that can save and load sessions.

    This class is meant to be subclassed, and the subclass should implement
    the following methods:
    - getSessionConfig
    - finishLoadConfig

    In a derived class's __init__ method, the __init__ method of this class
    should be called first, before any other initialisation.


    Properties of Note:
    -------------------
    self.settings
        This is a QSettings object that is used to save and load the session
        settings such as the light/dark theme, the session directory, etc.
    self.progress_windows
        This is a dictionary of ProgressTimerDialog objects, where the key is
        the name of the progress window.
    self.sessions_directory
        This is the path to the directory where the session folders are saved.
        This is set by the user using the menu option:
        "Settings > Set Session Directory".
        Inside the folder specified by the user, there will be a
        folder called self.sessions_directory_name, which is where
        the session folders are saved.
        So self.sessions_directory will be:
        <user selected directory>/<self.sessions_directory_name>
    '''

    def __init__(self, title, app_name, settings_name=None,
                 organisation_name=None, **kwargs):

        super(MainWindowWithSessionManagement, self).__init__(title, app_name, settings_name, organisation_name, **kwargs)

        self._setupMainWindowWithSessionManagement()


    def _setupMainWindowWithSessionManagement(self):
        '''Setup the session main window.
        
        This is called by the __init__ method, and should not be called by the
        user.
        '''               

        # This is the name of the directory where the session folders are saved
        # This will be within a directory that is picked by the user
        # i.e. the location of the session folders will be:
        # <user selected directory>/<self.sessions_directory_name>
        self.sessions_directory_name = self.app_name.replace(
            " ", "-") + "-Sessions"
        self.sessions_directory = None

        self.setupSession()

        self.should_really_close = False


    # Create the menu ----------------------------------------------------------

    def createMenu(self):
        '''Create the menu bar, with the following options:

        File
            Save
                This will save the current session
            Save & Exit
                This will save the current session and exit the application
            Exit
                This will exit the application without saving the current session

        Settings
            App Settings
                This will open a dialog to change the application settings, such as
                the light/dark theme
            Session Directory
                This will open a dialog to select the path where the session folders
                are saved

        Sets
        ----
        self.menu_bar: QMenuBar
            The menu bar
        self.menus: dict
            A dictionary of the menu names and the corresponding QMenu objects

        '''

        menu_bar = self.menuBar()

        # If we add the menus this way, then the menuBar takes ownership of the menus:
        file_menu = menu_bar.addMenu("File")

        save_action = QAction("Save", self)
        save_action.triggered.connect(
            partial(self.createSaveWindow, event="SaveEvent"))
        file_menu.addAction(save_action)

        save_exit_action = QAction("Save + Exit", self)
        save_exit_action.triggered.connect(self.close)
        file_menu.addAction(save_exit_action)

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        settings_menu = menu_bar.addMenu("Settings")

        app_settings_action = QAction("App Settings", self)
        app_settings_action.triggered.connect(self.createAppSettingsDialog)
        settings_menu.addAction(app_settings_action)

        session_folder_action = QAction("Set Session Directory", self)
        session_folder_action.triggered.connect(
            lambda: self.createSessionsDirectorySelectionDialog(new_session=False))
        settings_menu.addAction(session_folder_action)

        menus = {
            "File": file_menu,
            "Settings": settings_menu
        }

        self.menu_bar = menu_bar
        self.menus = menus

    # Loading Sessions ---------------------------------------------------------

    def setupSession(self):
        '''
        Loads the appropriate dialogs to allow users to make selections about loading sessions:

        If this is the first time they open the application, they will be asked to select a directory
        to store the sessions in. This directory will be stored in the settings, and will be used
        as the default directory for future sessions. Then, if any sessions exist already in that directory,
        they will be asked if they want to load one of those sessions, if not, a new session will be created.

        If this is not the first time they open the application, they will be asked to select a session
        to load, if any sessions are present in the directory saved in the settings. If they select a session,
        it will be loaded. If they select "New Session", a new session will be created.
        '''

        if self.settings.value('sessions_folder') is None:
            # get user to select directory, then within that directory we create a folder called session_folder_name,
            # which will then contain all of the session folders.
            self.createSessionsDirectorySelectionDialog(new_session=True)
        else:
            session_folder_name = self.settings.value('sessions_folder')
            if not os.path.exists(session_folder_name):
                self.createSessionsDirectorySelectionDialog(new_session=True)
            else:
                self.sessions_directory = session_folder_name
                self.createSessionSelector()

    def createSessionSelector(self):
        ''''
        Create a LoadSessionDialog, populated with the names of the sessions
        saved in the current working directory.

        If no sessions exist, create a new session
        '''
        zip_folders = []
        for _, _, f in os.walk(self.sessions_directory):
            for _file in f:
                if '.zip' in _file:
                    array = _file.split("_")
                    if (len(array) > 1):
                        date = _file.split("_")[-1]
                        name = _file.replace(
                            "_" + date, "") + " " + date.strip(".zip")
                        zip_folders.append(name)

        if len(zip_folders) == 0:
            self.loadSessionNew()
        else:
            self.SessionSelectionWindow = self.createLoadSessionDialog(
                zip_folders)

    def createLoadSessionDialog(self, zip_folders):
        '''
        Create a LoadSessionDialog, populated with the names of the sessions
        saved in the current working directory.
        '''
        dialog = LoadSessionDialog(
            parent=self, location_of_session_files=self.sessions_directory)
        dialog.widgets['select_session_field'].addItems(zip_folders)
        dialog.Ok.clicked.connect(self.loadSessionLoad)
        dialog.Select.clicked.connect(
            lambda: self.selectLoadSessionsDirectorySelectedInSessionSelector(dialog))
        dialog.Cancel.clicked.connect(self.loadSessionNew)
        dialog.open()

        return dialog

    def selectLoadSessionsDirectorySelectedInSessionSelector(self, load_session_dialog):
        '''
        When the user selects the "Select Directory for Loading Sessions" button in the LoadSessionDialog, this method
        will be called. It will close the LoadSessionDialog, and open a SessionDirectorySelectionDialog
        to allow the user to select a directory in which the list of sessions will be loaded from.
        '''
        load_session_dialog.close()
        self.createSessionsDirectorySelectionDialog(new_session=True)

    def createSessionsDirectorySelectionDialog(self, new_session=False):
        '''
        Create a SessionDirectorySelectionDialog, which allows the user to select
        a directory in which the sessions folder will be created.

        Opens the dialog, and connects the Ok button to the appropriate method

        Parameters
        ----------
        new_session : bool
            Whether or not this method is called straight after the user has opened the application
        '''
        session_folder_selection_dialog = SessionDirectorySelectionDialog(
            parent=self, app_name=self.app_name)

        if new_session:
            # Move on to creating directory and loading session names
            session_folder_selection_dialog.Ok.clicked.connect(
                lambda: self.onSessionDirectorySelectionDialogOkNewSession(session_folder_selection_dialog))
        else:
            # Splitting the path and the folder name, means that we only display the folder name that the user has selected
            # and not the full path including the self.sessions_directory_name:
            session_folder_selection_dialog.Ok.clicked.connect(
                lambda: self.onSessionDirectorySelectionDialogOkInSession(session_folder_selection_dialog))
            session_folder_selection_dialog.Cancel.setEnabled(True)
            session_folder_selection_dialog.Cancel.clicked.connect(
                session_folder_selection_dialog.close)

        if self.sessions_directory is not None:
            session_folder_selection_dialog.getWidget('selected_dir', 'label').setText(
                os.path.split(self.sessions_directory)[0])
            session_folder_selection_dialog.selected_dir = os.path.split(
                self.sessions_directory)[0]

        session_folder_selection_dialog.open()

        return session_folder_selection_dialog

    def onSessionDirectorySelectionDialogOkNewSession(self, session_folder_selection_dialog):
        '''
        Runs if the user selects Ok on the SessionDirectorySelectionDialog when creating a new session
        '''
        if session_folder_selection_dialog.selected_dir is not None:
            self.createSessionsDirectoryAndMakeSessionSelector(
                session_folder_selection_dialog.selected_dir)
            session_folder_selection_dialog.close()

    def onSessionDirectorySelectionDialogOkInSession(self, session_folder_selection_dialog):
        '''
        Runs if the user selects Ok on the SessionDirectorySelectionDialog when in a session
        '''
        if session_folder_selection_dialog.selected_dir is not None:
            self.createSessionsDirectory(
                session_folder_selection_dialog.selected_dir)
        session_folder_selection_dialog.close()

    def createSessionsDirectoryAndMakeSessionSelector(self, user_chosen_directory):
        '''
        Creates the sessions directory, and then calls the method to create the session selector
        '''
        self.createSessionsDirectory(user_chosen_directory)
        self.createSessionSelector()

    def createSessionsDirectory(self, user_selected_directory):
        '''
        If the directory selected by the user does not exist, create it, and then create a folder
        called sessions_directory_name within it.
        Move into the sessions_directory_name folder, and store the path to that folder in the settings.
        Also stores the path to self.sessions_directory_name
        '''
        # If the user has selected the sessions_directory_name folder, we want to move up a directory
        # before looking for the sessions_directory_name folder within that directory.
        # This is necessary because if the sessions_directory_name folder already exists and contains
        # sessions, we don't want to create another sessions_directory_name folder within it, as then the
        # existing sessions won't be available for loading.

        if os.path.basename(user_selected_directory) == self.sessions_directory_name:
            user_selected_directory = os.path.dirname(user_selected_directory)
        else:
            if not os.path.isdir(user_selected_directory):
                os.mkdir(user_selected_directory)

        sessions_directory = os.path.abspath(os.path.join(
            user_selected_directory, self.sessions_directory_name))

        if not os.path.isdir(sessions_directory):
            os.mkdir(sessions_directory)
        self.settings.setValue('sessions_folder', sessions_directory)
        self.sessions_directory = sessions_directory

    def loadSessionNew(self):
        '''
        Loads a new session
        '''
        self.createSessionFolder()
        if hasattr(self, 'SessionSelectionWindow'):
            self.SessionSelectionWindow.close()

    def loadSessionLoad(self):
        '''
        Loads a session from a zip file
        '''

        folder_name = self.SessionSelectionWindow.widgets['select_session_field'].currentText(
        )

        process_name = "Loading Session: {}".format(folder_name)

        # Create progress bar which just has an increasing timer:
        self.process_finished = False
        self.createUnknownProgressWindow(process_name)
        config_worker = Worker(self.loadSessionConfig, folder=folder_name)
        config_worker.signals.finished.connect(
            lambda: self.finishLoadConfig(process_name))
        self.threadpool.start(config_worker)
        self.SessionSelectionWindow.close()

    def createSessionFolder(self):
        '''
        Creates a session folder with the name:
        <app_name>-<date>-<time>
        '''
        date_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
        session_folder_name = '{}-{}'.format(self.app_name, date_time)
        session_folder_path = os.path.join(
            self.sessions_directory, session_folder_name)
        os.mkdir(session_folder_path)
        self.current_session_folder = os.path.abspath(session_folder_path)

    def loadSessionConfig(self, folder, **kwargs):
        '''
        Unzips a session folder and saves the contents of the .json session file to
        self.config.


        Parameters
        ----------
        folder : str
            The folder to load.
        '''

        selected_text = folder
        date_and_time = selected_text.split(' ')[-1]
        selected_folder = ""

        for _, _, f in os.walk(self.sessions_directory):
            for _file in f:
                if date_and_time + '.zip' in _file:
                    selected_folder = os.path.join(
                        self.sessions_directory, _file)
                    break

        shutil.unpack_archive(selected_folder, selected_folder[:-4])
        loaded_folder = selected_folder[:-4]
        self.current_session_folder = loaded_folder

        json_filename = os.path.join(
            self.current_session_folder, "session.json")

        with open(json_filename) as tmp:
            self.config = json.load(tmp)

    def finishLoadConfig(self, process_name):
        '''
        Called when the config file has been loaded.
        In child classes, you will want to re-implement this function to load
        the GUI elements.'''
        self.finishProcess(process_name)

    def finishProcess(self, process_name):
        '''
        Called when a process has finished.
        Closes the progress bar and sets the process_finished flag to True.
        '''
        self.process_finished = True
        self.progress_windows[process_name].close()

    # Handling Closing And Saving Sessions -------------------------------------

    def closeEvent(self, event):
        '''
        Overwrites the default closeEvent to prompt the user to save the session before closing.

        This method occurs when we call self.close() or when the user clicks the X button on the window.
        '''

        # Need to check that we are not inside the current session folder, as this will either be
        # deleted or moved to a new location.

        if self.current_session_folder in os.path.abspath(os.getcwd()):
            # Move out into the folder that contains the session folders:
            os.chdir(self.sessions_directory)

        if not self.should_really_close:
            self.createSaveWindow(event)
            event.ignore()

    def createSaveWindow(self, event):
        ''''
        Creates a dialog which asks the user if they would like to save the session before closing.

        If the event is a QCloseEvent, then the whole app will always be closed, but the user
        first has an option to save the session.

        If the event is anything else, then the user has the option to save the session, but
        the app will not be closed.

        Parameters
        ----------
        event: 
            The event which triggered the dialog.
        '''
        self.should_really_close = False
        dialog = SaveSessionDialog(parent=self, title='Save Session')
        self.SaveWindow = dialog

        # We have 2 instances of the window.
        if isinstance(event, QCloseEvent):
            # This is the case where we are quitting the app and the window asks if we
            # would like to save
            dialog.Cancel.clicked.connect(
                lambda: self.saveQuitDialogRejected(dialog))
            dialog.Ok.clicked.connect(
                lambda: self.saveQuitDialogAccepted(dialog))
            dialog.Cancel.setText('Quit without saving')
        else:
            # This is the case where we are just choosing to 'Save' in the file menu
            # so we never quit the app.
            dialog.Cancel.clicked.connect(
                lambda: self.saveDialogRejected(dialog))
            dialog.Ok.clicked.connect(lambda: self.saveDialogAccepted(dialog))
            dialog.Cancel.setText('Cancel')

        dialog.open()

    def saveDialogAccepted(self, dialog):
        '''
        Called when the user clicks 'Save' in the save dialog.
        This saves the session and then closes the dialog.
        '''
        compress = dialog.widgets['compress_field'].isChecked()
        dialog.close()
        session_name = dialog.widgets['session_name_field'].text()
        self.runSaveSessionWorker(session_name, compress, None)

    def saveDialogRejected(self, dialog):
        '''
        Called when the user clicks 'Cancel' in the save dialog.
        This closes the dialog.
        '''
        dialog.close()

    def saveQuitDialogAccepted(self, dialog):
        '''
        Called when the user clicks 'Save' in the save and quit dialog.
        This saves the session and then closes the app.
        '''
        self.should_really_close = True
        compress = dialog.widgets['compress_field'].isChecked()
        session_name = dialog.widgets['session_name_field'].text()
        dialog.close()
        self.runSaveSessionWorker(session_name, compress, QCloseEvent())

    def saveQuitDialogRejected(self, dialog):
        '''
        Called when the user clicks 'Quit without saving' in the save and quit dialog.
        This closes the app.
        '''
        self.removeTemp()  # remove tempdir for this session.
        dialog.close()
        self.should_really_close = True
        self.close()

    def runSaveSessionWorker(self, session_name, compress, event):
        '''
        Runs self.saveSession in a thread.

        When the thread is finished, it calls self.closeSaveWindow, or self.removeTempAndClose
        depending on the type of event.

        If the event is a QCloseEvent, then the whole app will always be closed, by calling
        self.removeTempAndClose.

        If the event is anything else, then the app will not be closed, by calling
        self.closeSaveWindow.
        '''
        process_name = 'Save Session'

        self.process_finished = False
        self.createUnknownProgressWindow(
            process_name, "Saving", "Saving Session")

        saveSession_worker = Worker(self.saveSession, session_name, compress)
        if type(event) == QCloseEvent:
            saveSession_worker.signals.finished.connect(
                lambda: self.removeTempAndClose(process_name))
        else:
            saveSession_worker.signals.finished.connect(
                lambda: self.closeSaveWindow(process_name))
        self.threadpool.start(saveSession_worker)

    def saveSession(self, session_name, compress, **kwargs):
        '''
        Save the session to a zip file
        The zip file contains the session.json file and the nxs files, and any files
        already in the session folder
        '''
        self.moveSessionFolder(session_name)
        self.saveSessionConfigToJson()
        zip_directory(self.current_session_folder, compress)

    def getSessionConfig(self):
        '''
        Returns the session config, which is a dictionary containing the session name,
        the datetime, the list of files in the session folder, the config of all the
        widgets in the app.

        This must be re-implemented in the child class, to perform the above.
        '''
        return {}

    def moveSessionFolder(self, session_name):
        '''
        Creates a new session folder, and moves the current session folder to it.
        Saves new session folder as self.current_session_folder
        Moves into the new session folder
        '''

        now_string = datetime.now().strftime("%d-%m-%Y-%H-%M")
        new_folder_to_save_to = os.path.join(
            self.sessions_directory, session_name + "_" + now_string)
        shutil.move(self.current_session_folder, new_folder_to_save_to)
        self.current_session_folder = new_folder_to_save_to

    def saveSessionConfigToJson(self):
        '''
        Saves the session config to a json file in the session folder: self.current_session_folder
        '''
        session_file = os.path.join(
            self.current_session_folder, "session.json")

        self.config = self.getSessionConfig()

        self.config['datetime'] = datetime.now().strftime("%d-%m-%Y-%H-%M")

        # Session file will always have the same name.
        # If a session has been reloaded, and saved again, this will overwrite the old session file.

        with open(session_file, "w+") as f:
            json.dump(self.config, f)

    def removeTempAndClose(self, process_name):
        '''
        Removes the temp directory for this session, and closes the app.
        '''
        self.removeTemp()
        self.finishProcess(process_name)
        self.should_really_close = True
        self.close()

    def removeTemp(self):
        '''
        Removes the temp directory for this session.
        '''
        if hasattr(self, 'current_session_folder'):
            try:
                shutil.rmtree(self.current_session_folder)
            except PermissionError as e:
                dialog = ErrorDialog(self, message=str(e))
                dialog.exec_()
                self.removeTemp()

    def closeSaveWindow(self, process_name):
        '''
        Closes the save window and moves back to the session folder.
        '''
        # move back to session dir in case we moved
        # out of it for zipping etc. :
        self.finishProcess(process_name)
        self.SaveWindow.close()
