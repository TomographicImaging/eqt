import json
import os
import shutil
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch

from PySide2.QtCore import QSettings, QThreadPool
from PySide2.QtWidgets import QMenu, QMenuBar

import eqt
from eqt.io import zip_directory
from eqt.ui.MainWindowWithSessionManagement import MainWindowWithSessionManagement

from . import skip_ci


@skip_ci
class TestMainWindowWithSessionManagementInit(unittest.TestCase):
    '''
    Tests the init method of the MainWindowWithSessionManagement class
    '''
    def setUp(self):
        # Testing the init method, so don't call init in the setUp
        self.title = "title"
        self.app_name = "App Name"
        MainWindowWithSessionManagement.createSessionsDirectorySelectionDialog = mock.MagicMock()

    def test_init_sets_title_and_app_name(self):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        assert smw is not None
        self.assertEqual(smw.windowTitle(), "title")
        self.assertEqual(smw.app_name, "App Name")

    def test_init_creates_threadpool(self):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        assert smw.threadpool is not None
        assert (isinstance(smw.threadpool, QThreadPool))

    def test_init_creates_settings(self):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        assert smw.settings is not None
        assert (isinstance(smw.settings, QSettings))
        self.assertEqual(smw.settings.organizationName(), self.app_name)
        self.assertEqual(smw.settings.applicationName(), self.app_name)

    def test_init_creates_settings_when_settings_name_given(self):
        settings_name = "settings_name"
        smw = MainWindowWithSessionManagement(self.title, self.app_name, settings_name)
        assert smw.settings is not None
        assert (isinstance(smw.settings, QSettings))
        self.assertEqual(smw.settings.organizationName(), self.app_name)
        self.assertEqual(smw.settings.applicationName(), settings_name)

    @patch('eqt.ui.MainWindowWithSessionManagement.MainWindowWithSessionManagement.setAppStyle')
    def test_init_calls_setAppStyle(self, mock_setAppStyle):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        smw.setAppStyle.assert_called_once()

    @patch('eqt.ui.MainWindowWithSessionManagement.MainWindowWithSessionManagement.createMenu',
           return_value=(1, {}))
    def test_init_calls_createMenu(self, mock_menu_bar):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        smw.createMenu.assert_called_once()

    def test_sessions_directory_name_set(self):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        self.assertEqual(smw.sessions_directory_name, "App-Name-Sessions")

    def test_init_initialises_vars(self):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        self.assertEqual(smw.sessions_directory, None)
        self.assertEqual(smw.should_really_close, False)
        self.assertEqual(smw.progress_windows, {})

    @patch('eqt.ui.MainWindowWithSessionManagement.MainWindowWithSessionManagement.setupSession')
    def test_init_calls_setUpSession(self, mock_setupSession):
        smw = MainWindowWithSessionManagement(self.title, self.app_name)
        smw.setupSession.assert_called_once()


@skip_ci
class TestMainWindowWithSessionManagementMenuBar(unittest.TestCase):
    '''
    Tests the expected menu bar is created
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)

    def test_createMenu_sets_menu_bar_and_menus(self):
        # first remove the menu bar and menus which are created in the init
        del self.smw.menu_bar
        del self.smw.menus
        self.smw.createMenu()
        assert hasattr(self.smw, "menu_bar")
        assert hasattr(self.smw, "menus")
        assert isinstance(self.smw.menu_bar, QMenuBar)
        assert isinstance(self.smw.menus, dict)
        # dict should contain the expected menus
        assert "File" in self.smw.menus
        assert "Settings" in self.smw.menus
        assert isinstance(self.smw.menus["File"], QMenu)
        assert isinstance(self.smw.menus["Settings"], QMenu)

    def test_menu_has_file_and_settings_menu(self):
        actions = self.smw.menu_bar.actions()
        assert actions[0].text() == "File"
        assert actions[1].text() == "Settings"

    def test_file_menu_has_expected_actions(self):
        menus = self.smw.menu_bar.findChildren(QMenu)
        file_menu = menus[0]
        assert file_menu.actions()[0].text() == "Save"
        assert file_menu.actions()[1].text() == "Save + Exit"
        assert file_menu.actions()[2].text() == "Exit"

    def test_settings_menu_has_expected_actions(self):
        menus = self.smw.menu_bar.findChildren(QMenu)
        settings_menu = menus[1]
        self.assertEqual(settings_menu.actions()[0].text(), "App Settings")
        self.assertEqual(settings_menu.actions()[1].text(), "Set Session Directory")


@skip_ci
class TestMainWindowWithSessionManagementSetupSession(unittest.TestCase):
    '''
    Tests the setupSession method of the MainWindowWithSessionManagement class

    This method is responsible for setting up the session directory and session selector
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)

    def test_setupSession_when_sessions_folder_setting_is_None(self):
        self.smw.settings = mock.MagicMock()
        self.smw.createSessionsDirectorySelectionDialog = mock.MagicMock()
        self.smw.createSessionSelector = mock.MagicMock()
        self.smw.settings.value = mock.MagicMock(return_value=None)
        self.smw.setupSession()
        self.smw.createSessionsDirectorySelectionDialog.assert_called_once_with(new_session=True)
        self.smw.createSessionSelector.assert_not_called()

    def test_setupSession_when_sessions_folder_setting_is_not_None(self):
        self.smw.settings = mock.MagicMock()
        self.smw.createSessionsDirectorySelectionDialog = mock.MagicMock()
        self.smw.createSessionSelector = mock.MagicMock()
        session_folder_name = "session_folder_name"
        os.mkdir(session_folder_name)
        try:
            self.smw.settings.value = mock.MagicMock(return_value=session_folder_name)
            self.smw.setupSession()
            self.smw.createSessionsDirectorySelectionDialog.assert_not_called()
            self.smw.createSessionSelector.assert_called_once()
            self.assertEqual(self.smw.sessions_directory, session_folder_name)

        except Exception as e:
            raise e

        finally:
            if os.path.basename(os.getcwd()) == session_folder_name:
                os.chdir("..")
                os.rmdir(session_folder_name)

            else:
                os.rmdir(session_folder_name)

    def test_setupSession_when_given_nonexistent_sessions_folder(self):
        self.smw.settings = mock.MagicMock()
        self.smw.createSessionsDirectorySelectionDialog = mock.MagicMock()
        self.smw.createSessionSelector = mock.MagicMock()
        session_folder_name = "session_folder_name"
        self.smw.settings.value = mock.MagicMock(return_value=session_folder_name)
        self.smw.setupSession()
        self.smw.createSessionsDirectorySelectionDialog.assert_called_once_with(new_session=True)
        self.smw.createSessionSelector.assert_not_called()


@skip_ci
class TestMainWindowWithSessionManagementCreateSessionSelector(unittest.TestCase):
    '''
    Tests the createSessionSelector method of the MainWindowWithSessionManagement class

    This method is responsible for creating the session selector if any sessions exist,
    or calling a method to create a new session if no sessions exist
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)
        if not os.path.isdir("Test_Folder"):
            os.mkdir("Test_Folder")
        os.chdir("Test_Folder")
        os.mkdir("Session Folder")
        self.smw.sessions_directory = "."

    def test_createSessionSelector_when_no_session_zips_exist(self):
        self.smw.loadSessionNew = mock.MagicMock()
        eqt.ui.SessionDialogs.LoadSessionDialog = mock.MagicMock()
        self.smw.createSessionSelector()
        self.smw.loadSessionNew.assert_called_once()
        eqt.ui.SessionDialogs.LoadSessionDialog.assert_not_called()

    def test_createSessionSelector_when_session_zips_exist(self):
        # Make 2 zip files in the sessions directory:
        os.chdir("Session Folder")
        shutil.make_archive("_session1_08-02-22", "zip")
        shutil.make_archive("session_2_08-02-22", "zip")
        os.chdir("..")

        zip_folders = ["_session1 08-02-22", "session_2 08-02-22"]

        self.smw.createLoadSessionDialog = mock.MagicMock()
        self.smw.loadSessionNew = mock.MagicMock()
        self.smw.createSessionSelector()
        self.smw.loadSessionNew.assert_not_called()

        try:
            self.smw.createLoadSessionDialog.assert_called_once_with(zip_folders)
        except AssertionError:
            # zip files could be returned in reverse order
            self.smw.createLoadSessionDialog.assert_called_once_with(zip_folders[::-1])

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree("Test_Folder")


@skip_ci
class TestSelectLoadSessionsDirectorySelectedInSessionSelector(unittest.TestCase):
    '''
    Tests the `selectLoadSessionsDirectorySelectedInSessionSelector` method of the
    `MainWindowWithSessionManagement` class

    This method should close the passed dialog, and call
    `createSessionsDirectorySelectionDialog(new_session=True)`
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)
        self.load_session_dialog = mock.MagicMock()
        self.load_session_dialog.close = mock.MagicMock()
        self.smw.createSessionsDirectorySelectionDialog = mock.MagicMock()

    def test_selectLoadSessionsDirectorySelectedInSessionSelector(self):
        self.smw.selectLoadSessionsDirectorySelectedInSessionSelector(self.load_session_dialog)
        assert self.load_session_dialog.close.called_once()
        assert self.smw.createSessionsDirectorySelectionDialog.called_once_with(new_session=True)


@skip_ci
class TestCreateSessionFolder(unittest.TestCase):
    '''
    Tests the createSessionFolder method of the MainWindowWithSessionManagement class

    This method is responsible for creating a folder for the session and moving into it
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"

        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)

        os.mkdir("Test_Folder")
        os.chdir("Test_Folder")
        self.date_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    def test_createSessionFolder(self):
        session_folder_name = "app_name-" + self.date_time
        # We need to mock the sessions_directory method, as it has not been set up yet
        # We want the session folder to be made in the current directory for this test
        self.smw.sessions_directory = "."
        self.smw.createSessionFolder()
        assert os.path.exists(session_folder_name)

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree("Test_Folder")


@skip_ci
class TestLoadSessionConfig(unittest.TestCase):
    '''
    Tests the loadSessionConfig method of the `MainWindowWithSessionManagement` class.

    This method is responsible for unzipping a session folder and saving the contents
    of the `.json` session file to `MainWindowWithSessionManagement.config`.
    '''
    def setUp(self):
        '''
        Create a session zip file, which contains a session.json file'''
        os.mkdir("Test_Folder")
        os.chdir("Test_Folder")

        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)
        self.smw.sessions_directory = "Sessions Folder"
        self.session_folder = os.path.join(self.smw.sessions_directory,
                                           "app name 01-01-2020-00-00-00")

        self.config = {
            'test_key': 'test_value', 'test_key2': 'test_value2', 'test_int_key': 1,
            'test_float_key': 1.0, 'test_bool_key': True, 'test_list_key': [1, 2, 3],
            'test_dict_key': {'test_key': 'test_value'}}

        os.mkdir(self.smw.sessions_directory)
        os.mkdir(self.session_folder)

        session_file = os.path.join(self.session_folder, "session.json")
        with open(session_file, "w+") as f:
            json.dump(self.config, f)

    def test_loadSessionConfig(self):
        zip_directory(self.session_folder, compress=False)
        self.smw.loadSessionConfig(self.session_folder)
        self.assertEqual(self.config, self.smw.config)

    def tearDown(self):
        os.chdir("..")
        try:
            shutil.rmtree("Test_Folder")
        except Exception:
            os.chdir("..")
            shutil.rmtree("Test_Folder")


@skip_ci
class TestSaveSession(unittest.TestCase):
    '''
    Tests:
    - saveSession method of the MainWindowWithSessionManagement class
    - moveSessionFolder method of the MainWindowWithSessionManagement class
    - saveSessionConfigToJson method of the MainWindowWithSessionManagement class

    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)
        self.session_name = self.app_name

    @mock.patch('eqt.ui.MainWindowWithSessionManagement.zip_directory')
    def test_saveSession(self, mock_zip_directory):
        self.smw.moveSessionFolder = mock.MagicMock()
        self.smw.saveSessionConfigToJson = mock.MagicMock()
        self.smw.current_session_folder = mock.MagicMock()
        self.smw.saveSession(self.session_name, compress=False)
        self.smw.moveSessionFolder.assert_called_once_with(self.session_name)
        self.smw.saveSessionConfigToJson.assert_called_once()
        mock_zip_directory.assert_called_once_with(self.smw.current_session_folder, False)

    def test_moveSessionFolder(self):
        os.mkdir("Test_Folder")
        new_folder_to_save_to = os.path.join(
            "Test_Folder", self.session_name + "_" + datetime.now().strftime("%d-%m-%Y-%H-%M"))

        # Make the current session folder, with a test file inside it:

        self.smw.sessions_directory = os.path.abspath("Test_Folder")
        current_session_folder = os.path.join(self.smw.sessions_directory,
                                              "Current Session Folder")
        os.mkdir(current_session_folder)
        # Write file inside the folder:
        with open(os.path.join(current_session_folder, "test_file.txt"), "w+") as f:
            f.write("test")
        # os.chdir("Current Session Folder")
        self.smw.current_session_folder = current_session_folder

        try:
            self.smw.moveSessionFolder(self.session_name)
            self.assertEqual(os.path.abspath(self.smw.current_session_folder),
                             os.path.abspath(new_folder_to_save_to))
            self.assertTrue(os.path.exists(new_folder_to_save_to))
            self.assertTrue(os.path.exists(os.path.join(new_folder_to_save_to, "test_file.txt")))
            self.assertFalse(os.path.exists("Current Session Folder"))
            self.assertFalse(
                os.path.exists(os.path.join("Current Session Folder", "test_file.txt")))

        except Exception as e:
            raise e

        finally:
            shutil.rmtree("Test_Folder")

    def test_saveSessionConfigToJson(self):

        self.config = {
            'test_key': 'test_value', 'test_key2': 'test_value2', 'test_int_key': 1,
            'test_float_key': 1.0, 'test_bool_key': True, 'test_list_key': [1, 2, 3],
            'test_dict_key': {'test_key': 'test_value'}}

        config = {}
        config.update(self.config)

        # datetime gets added in the saveSessionConfigToJson method:
        self.config['datetime'] = datetime.now().strftime("%d-%m-%Y-%H-%M")

        self.smw.getSessionConfig = mock.MagicMock(return_value=config)

        os.mkdir("Test_Folder")
        os.chdir("Test_Folder")
        self.smw.current_session_folder = "."
        try:
            self.smw.saveSessionConfigToJson()
            session_file = os.path.join(os.getcwd(), "session.json")
            with open(session_file, "r") as f:
                config = json.load(f)
            self.assertEqual(config, self.config)
        except Exception as e:
            raise e
        finally:
            os.chdir("..")
            shutil.rmtree("Test_Folder")


@skip_ci
class TestRemoveTempMethods(unittest.TestCase):
    '''
    Tests:
    - removeTempAndClose method of the MainWindowWithSessionManagement class
    - removeTemp method of the MainWindowWithSessionManagement class
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)

    def test_removeTemp_when_current_session_folder_exists(self):
        try:
            self.smw.current_session_folder = "Test Session Folder"
            os.mkdir(self.smw.current_session_folder)
            self.smw.removeTemp()
            self.assertFalse(os.path.exists(self.smw.current_session_folder))
        except Exception as e:
            try:
                shutil.rmtree(self.smw.current_session_folder)
            except Exception:
                raise e

    def test_removeTemp_when_current_session_folder_does_not_exist(self):
        self.smw.current_session_folder = "Test Session Folder"
        # Test this raises a FileNotFoundError:
        with self.assertRaises(FileNotFoundError):
            self.smw.removeTemp()

    def test_removeTempAndClose(self):
        process_name = "Test Process"
        self.smw.removeTemp = mock.MagicMock()
        self.smw.close = mock.MagicMock()
        self.smw.finishProcess = mock.MagicMock()
        self.smw.should_really_close = False
        self.smw.removeTempAndClose(process_name)
        self.smw.removeTemp.assert_called_once()
        self.smw.finishProcess.assert_called_once_with(process_name)
        self.smw.close.assert_called_once()
