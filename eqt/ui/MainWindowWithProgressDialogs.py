import qdarkstyle
from PySide2.QtCore import QSettings, QThreadPool
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import QAction, QMainWindow
from qdarkstyle.dark.palette import DarkPalette
from qdarkstyle.light.palette import LightPalette

from eqt.ui.ProgressTimerDialog import ProgressTimerDialog
from eqt.ui.SessionDialogs import (AppSettingsDialog)


class MainWindowWithProgressDialogs(QMainWindow):
    '''
    A base class for a main window, with a menu bar, and ability to 
    create ProgressTimerDialogs.
    In a derived class's __init__ method, the __init__ method of this class
    should be called first, before any other initialisation.

    Properties of Note:
    -------------------
    self.settings
        This is a QSettings object that is used for
        settings such as the light/dark theme.
    self.progress_windows
        This is a dictionary of ProgressTimerDialog objects, where the key is
        the name of the progress window.
    '''

    def __init__(self, title, app_name, settings_name=None,
                 organisation_name=None, **kwargs):

        super(MainWindowWithProgressDialogs, self).__init__(**kwargs)

        self.setWindowTitle(title)
        self.app_name = app_name
        self.threadpool = QThreadPool()

        if settings_name is None:
            settings_name = app_name
        if organisation_name is None:
            organisation_name = app_name

        self.settings = QSettings(organisation_name, settings_name)

        self.setAppStyle()

        self.createMenu()

        self._progress_windows = {}
  
    @property
    def progress_windows(self):
        return self._progress_windows 

    # Create the menu ----------------------------------------------------------

    def createMenu(self):
        '''Create the menu bar, with the following options:

        File
            Exit
                This will exit the application without saving the current session

        Settings
            App Settings
                This will open a dialog to change the application settings, such as
                the light/dark theme

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

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        settings_menu = menu_bar.addMenu("Settings")

        app_settings_action = QAction("App Settings", self)
        app_settings_action.triggered.connect(self.createAppSettingsDialog)
        settings_menu.addAction(app_settings_action)

        menus = {
            "File": file_menu,
            "Settings": settings_menu
        }

        self.menu_bar = menu_bar
        self.menus = menus

    # Settings -----------------------------------------------------------------

    def setAppStyle(self):
        '''Sets app stylesheet, based on user's settings '''
        if self.settings.value("dark_mode") is None:
            self.settings.setValue("dark_mode", "true")
        if self.settings.value("dark_mode") == "true":
            style = qdarkstyle.load_stylesheet(palette=DarkPalette)
        else:
            style = qdarkstyle.load_stylesheet(palette=LightPalette)
        self.setStyleSheet(style)

    def createAppSettingsDialog(self):
        '''Create a dialog to change the application settings, such as the light/dark theme'''
        dialog = AppSettingsDialog(self)
        self.setAppSettingsDialogWidgets(dialog)
        dialog.Ok.clicked.connect(
            lambda: self.onAppSettingsDialogAccepted(dialog))
        dialog.Cancel.clicked.connect(dialog.close)
        dialog.open()

    def setAppSettingsDialogWidgets(self, dialog):
        '''Set the widgets on the app settings dialog, based on the
        current settings of the app'''
        if self.settings.value("dark_mode") == "true":
            dialog.widgets['dark_checkbox_field'].setChecked(True)
        else:
            dialog.widgets['dark_checkbox_field'].setChecked(False)

    def onAppSettingsDialogAccepted(self, dialog):
        '''This method is called when the user clicks
            "Ok" on the app settings dialog'''
        if dialog.widgets['dark_checkbox_field'].isChecked():
            self.settings.setValue("dark_mode", "true")
        else:
            self.settings.setValue("dark_mode", "false")
        self.setAppStyle()
        dialog.close()

    # Progress Bar -------------------------------------------------------------

    def createUnknownProgressWindow(self, process_name, title=None, detailed_text=None):
        '''
        Creates a progress bar with an unknown duration

        Instead of expecting to receive progress updates, this progress bar counts
        the number of seconds that have elapsed since it was created.

        This is useful for processes that take a long time, but for which we don't
        know how long they will take.

        Parameters
        ----------
        process_name : str
            The name of the process to be displayed in the progress bar
        title : str
            The title of the progress bar
        detailed_text : str
            The detailed text of the progress bar
        '''

        progress_window = ProgressTimerDialog(process_name, parent=self)
        self.saveReferenceToProgressWindow(progress_window, process_name)
        progress_window.show()

    def saveReferenceToProgressWindow(self, progress_window, process_name):
        self.progress_windows[process_name] = progress_window

    def finishProcess(self, process_name):
        '''
        Called when a process has finished.
        Closes the progress bar and sets the process_finished flag to True.
        '''
        self.process_finished = True
        self.progress_windows[process_name].close()




 

