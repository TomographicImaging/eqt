import json
import os
import shutil
import sys
import unittest
from datetime import datetime
from unittest import mock
from unittest.mock import patch

from PySide2.QtCore import QSettings, QThreadPool
from PySide2.QtWidgets import QApplication,QMenu, QMenuBar

import eqt
from eqt.io import zip_directory
from eqt.ui.SessionMainWindow import SessionMainWindow

# skip the tests on GitHub actions
if os.environ.get('CONDA_BUILD', '0') == '1':
    skip_as_conda_build = True
else:
    skip_as_conda_build = False


print ("skip_as_conda_build is set to ", skip_as_conda_build)

if not skip_as_conda_build:
    app = QApplication(sys.argv)
else:
    skip_test = True

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSessionMainWindowInit(unittest.TestCase):
    '''
    Tests the init method of the SessionMainWindow class
    '''

    def setUp(self):
        # Testing the init method, so don't call init in the setUp
        self.title = "title"
        self.app_name = "App Name"


    def test_init_sets_title_and_app_name(self):
        smw = SessionMainWindow(self.title, self.app_name)
        assert smw is not None
        self.assertEqual(smw.windowTitle(), "title")
        self.assertEqual(smw.app_name, "App Name")

    def test_init_creates_threadpool(self):
        smw = SessionMainWindow(self.title, self.app_name)
        assert smw.threadpool is not None
        assert(isinstance(smw.threadpool, QThreadPool))

    def test_init_creates_settings(self):
        smw = SessionMainWindow(self.title, self.app_name)
        assert smw.settings is not None
        assert(isinstance(smw.settings, QSettings))
        self.assertEqual(smw.settings.organizationName(), self.title)
        self.assertEqual(smw.settings.applicationName(), self.title)

    def test_init_creates_settings_when_settings_name_given(self):
        settings_name="settings_name"
        smw = SessionMainWindow(self.title, self.app_name, settings_name)
        assert smw.settings is not None
        assert(isinstance(smw.settings, QSettings))
        self.assertEqual(smw.settings.organizationName(), settings_name)
        self.assertEqual(smw.settings.applicationName(), settings_name)

    @patch('eqt.ui.SessionMainWindow.SessionMainWindow.setAppStyle')
    def test_init_calls_setAppStyle(self, mock_setAppStyle):
        smw = SessionMainWindow(self.title, self.app_name)
        smw.setAppStyle.assert_called_once()

    @patch('eqt.ui.SessionMainWindow.SessionMainWindow.createMenu')
    def test_init_calls_createMenu(self, mock_menu_bar):  
        smw = SessionMainWindow(self.title, self.app_name)     
        assert smw.menu is not None
        smw.createMenu.assert_called_once()

    def test_sessions_directory_name_set(self):
        smw = SessionMainWindow(self.title, self.app_name)
        self.assertEqual(smw.sessions_directory_name, "App-Name-Sessions")
    
    def test_init_initialises_vars(self):
        smw = SessionMainWindow(self.title, self.app_name)
        self.assertEqual(smw.sessions_directory, None)
        self.assertEqual(smw.should_really_close, False)
        self.assertEqual(smw.progress_windows, {})

    @patch('eqt.ui.SessionMainWindow.SessionMainWindow.setupSession')
    def test_init_calls_setUpSession(self, mock_setupSession):
        smw = SessionMainWindow(self.title, self.app_name)
        smw.setupSession.assert_called_once()


@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSessionMainWindowMenuBar(unittest.TestCase):
    '''
    Tests the expected menu bar is created
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)

    def test_createMenu_returns_QMenuBar(self):
        assert self.smw.createMenu() is not None
        assert isinstance(self.smw.createMenu(), QMenuBar)

    def test_menu_has_file_and_settings_menu(self):
        actions = self.smw.menu.actions()
        assert actions[0].text() == "File"
        assert actions[1].text() == "Settings"

    def test_file_menu_has_expected_actions(self):
        menus = self.smw.menu.findChildren(QMenu)
        file_menu = menus[0]
        assert file_menu.actions()[0].text() == "Save"
        assert file_menu.actions()[1].text() == "Save + Exit"
        assert file_menu.actions()[2].text() == "Exit"


    def test_settings_menu_has_expected_actions(self):
        menus = self.smw.menu.findChildren(QMenu)
        settings_menu = menus[1]
        self.assertEqual(settings_menu.actions()[0].text(), "Set Session Directory")


@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSessionMainWindowSetupSession(unittest.TestCase):
    '''
    Tests the setupSession method of the SessionMainWindow class
    
    This method is responsible for setting up the session directory and session selector
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)

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
            # Should have moved us into the session folder:
            self.assertEqual(os.path.basename(os.getcwd()), session_folder_name)

        except Exception as e:
            raise e

        finally:
            if os.path.basename(os.getcwd()) == session_folder_name:
                os.chdir("..")
                os.rmdir(session_folder_name)
                
            else:
                os.rmdir(session_folder_name)

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSessionMainWindowCreateSessionSelector(unittest.TestCase):
    '''
    Tests the createSessionSelector method of the SessionMainWindow class
    
    This method is responsible for creating the session selector if any sessions exist,
    or calling a method to create a new session if no sessions exist
    '''
    
    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)
        os.mkdir("Test Folder")
        os.chdir("Test Folder")

    def test_createSessionSelector_when_no_session_zips_exist(self):
        self.smw.loadSessionNew = mock.MagicMock()
        eqt.ui.SessionDialogs.LoadSessionDialog = mock.MagicMock()
        self.smw.createSessionSelector()
        self.smw.loadSessionNew.assert_called_once()
        eqt.ui.SessionDialogs.LoadSessionDialog.assert_not_called()

    def test_createSessionSelector_when_session_zips_exist(self):
        # Make 2 zip files in the sessions directory:
        shutil.make_archive("_session1_08-02-22", "zip")
        shutil.make_archive("session_2_08-02-22", "zip")

        zip_folders = ["_session1 08-02-22", "session_2 08-02-22"]

        self.smw.createLoadSessionDialog = mock.MagicMock()
        self.smw.loadSessionNew = mock.MagicMock()
        self.smw.sessions_directory = mock.MagicMock()
        self.smw.createSessionSelector()
        self.smw.loadSessionNew.assert_not_called()

        # We do not know which order the zip files will be returned in, so we need to check both orders:
        try:
            self.smw.createLoadSessionDialog.assert_called_once_with(zip_folders)
        except AssertionError:
            self.smw.createLoadSessionDialog.assert_called_once_with(zip_folders[::-1])

    def tearDown(self):
        os.chdir("..")
        shutil.rmtree("Test Folder")

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSessionMainWindowCreateLoadSessionDialog(unittest.TestCase):
    '''
    Tests the createLoadSessionDialog method of the SessionMainWindow class
    
    This method is responsible for creating the load session dialog
    and populating it with the available sessions
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)
        self.smw.sessions_directory = mock.MagicMock()
        self.zip_folders = ["zip_folder_1", "zip_folder_2"]

    def test_createLoadSessionDialog_populates_session_dropdown(self):
        dialog = self.smw.createLoadSessionDialog(self.zip_folders)
        assert dialog is not None
        assert isinstance(dialog, eqt.ui.SessionDialogs.LoadSessionDialog)
        select_session_combo = dialog.getWidget('select_session')
        assert select_session_combo is not None
        items_in_combo = [select_session_combo.itemText(i) for i in range(select_session_combo.count())]
        assert items_in_combo == self.zip_folders
    
    def test_createLoadSessionDialog_connections(self):
        dialog = self.smw.createLoadSessionDialog(self.zip_folders)

        self.smw.loadSessionLoad = mock.MagicMock()
        self.smw.selectLoadSessionsDirectorySelectedInSessionSelector = mock.MagicMock()
        self.smw.loadSessionNew = mock.MagicMock()

        dialog = self.smw.createLoadSessionDialog(self.zip_folders)

        dialog.Ok.click()
        self.smw.loadSessionLoad.assert_called_once()

        dialog.Select.click()
        self.smw.selectLoadSessionsDirectorySelectedInSessionSelector.assert_called_with(dialog)

        dialog.Cancel.click()
        self.smw.loadSessionNew.assert_called_once()

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSelectLoadSessionsDirectorySelectedInSessionSelector(unittest.TestCase):
    '''
    Tests the selectLoadSessionsDirectorySelectedInSessionSelector method of the SessionMainWindow class
    
    This method sould close the passed dialog, and call the createSessionsDirectorySelectionDialog method
    with the new_session parameter set to True
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)
        self.load_session_dialog = mock.MagicMock()
        self.load_session_dialog.close = mock.MagicMock()
        self.smw.createSessionsDirectorySelectionDialog = mock.MagicMock()

    def test_selectLoadSessionsDirectorySelectedInSessionSelector(self):
        self.smw.selectLoadSessionsDirectorySelectedInSessionSelector(self.load_session_dialog)
        assert self.load_session_dialog.close.called_once()
        assert self.smw.createSessionsDirectorySelectionDialog.called_once_with(new_session=True)

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestCreateSessionFolder(unittest.TestCase):
    '''
    Tests the createSessionFolder method of the SessionMainWindow class
    
    This method is responsible for creating a folder for the session and moving into it
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        
        
        self.smw = SessionMainWindow(self.title, self.app_name)

        os.mkdir("Test Folder")
        os.chdir("Test Folder")
        self.date_time = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

    def test_createSessionFolder(self):
        session_folder_name = "app_name-" + self.date_time
        self.smw.createSessionFolder()
        self.assertEqual(os.path.basename(os.getcwd()), session_folder_name)

    def tearDown(self):
        os.chdir("..")
        try:
            shutil.rmtree("Test Folder")
        except:
            os.chdir("..")
            shutil.rmtree("Test Folder")

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestLoadSessionConfig(unittest.TestCase):
    '''
    Tests the loadSessionConfig method of the SessionMainWindow class
    
    This method is responsible for unzipping a session folder and saving the contents of the .json session file to
    SessionMainWindow.config.
    '''

    def setUp(self):
        '''
        Create a session zip file, which contains a session.json file'''
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)
        self.session_folder = "app name 01-01-2020-00-00-00"

        self.config = {'test_key': 'test_value', 'test_key2': 'test_value2',
            'test_int_key': 1, 'test_float_key': 1.0, 'test_bool_key': True,
            'test_list_key': [1, 2, 3], 'test_dict_key': {'test_key': 'test_value'}}

        import json

        os.mkdir("Test Folder")
        os.chdir("Test Folder")
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
            shutil.rmtree("Test Folder")
        except:
            os.chdir("..")
            shutil.rmtree("Test Folder")

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSaveSession(unittest.TestCase):
    '''
    Tests:
    - saveSession method of the SessionMainWindow class
    - moveSessionFolder method of the SessionMainWindow class
    - saveSessionConfigToJson method of the SessionMainWindow class
    
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)
        self.session_name = self.app_name


    @mock.patch('eqt.ui.SessionMainWindow.zip_directory')
    def test_saveSession(self, mock_zip_directory):
        self.smw.moveSessionFolder = mock.MagicMock()
        self.smw.saveSessionConfigToJson = mock.MagicMock()
        self.smw.current_session_folder = mock.MagicMock()
        self.smw.saveSession(self.session_name, compress=False)
        self.smw.moveSessionFolder.assert_called_once_with(self.session_name)
        self.smw.saveSessionConfigToJson.assert_called_once()
        mock_zip_directory.assert_called_once_with(self.smw.current_session_folder, False)

    def test_moveSessionFolder(self):
        os.mkdir("Test Folder")
        os.chdir("Test Folder")
        new_folder_to_save_to = self.session_name + "_" + datetime.now().strftime("%d-%m-%Y-%H-%M")

        # Make the current session folder, with a test file inside it:
        
        self.smw.sessions_directory = os.getcwd()
        os.mkdir("Current Session Folder")
        # Write file inside the folder:
        with open(os.path.join("Current Session Folder", "test_file.txt"), "w+") as f:
            f.write("test")
        os.chdir("Current Session Folder")
        self.smw.current_session_folder = os.getcwd()

        try:
            self.smw.moveSessionFolder(self.session_name)
            self.assertEqual(os.path.basename(self.smw.current_session_folder), new_folder_to_save_to)
            self.assertTrue(os.path.exists(new_folder_to_save_to))
            self.assertTrue(os.path.exists(os.path.join(new_folder_to_save_to, "test_file.txt")))
            self.assertFalse(os.path.exists("Current Session Folder"))
            self.assertFalse(os.path.exists(os.path.join("Current Session Folder", "test_file.txt")))

        except Exception as e:
            raise e

        finally:
            os.chdir("..")
            try:
                shutil.rmtree("Test Folder")
            except:
                os.chdir("..")
                shutil.rmtree("Test Folder")

    def test_saveSessionConfigToJson(self):

        self.config = {'test_key': 'test_value', 'test_key2': 'test_value2',
            'test_int_key': 1, 'test_float_key': 1.0, 'test_bool_key': True,
            'test_list_key': [1, 2, 3], 'test_dict_key': {'test_key': 'test_value'}}

        config = {}
        config.update(self.config)

        # datetime gets added in the saveSessionConfigToJson method:
        self.config['datetime'] = datetime.now().strftime("%d-%m-%Y-%H-%M")
        
        self.smw.getSessionConfig = mock.MagicMock(return_value=config)

        os.mkdir("Test Folder")
        os.chdir("Test Folder")
        self.smw.current_session_folder = "."
        try:
            self.smw.saveSessionConfigToJson()
            session_file = os.path.join(os.getcwd(), "session.json")
            with open(session_file, "r") as f:
                config = json.load(f)
            self.assertEqual(config, self.config)
            print(config)
        except Exception as e:
            raise e
        finally:
            os.chdir("..")
            shutil.rmtree("Test Folder")
        
@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestRemoveTempMethods(unittest.TestCase):
    '''
    Tests:
    - removeTempAndClose method of the SessionMainWindow class
    - removeTemp method of the SessionMainWindow class
    '''

    def setUp(self):
        self.title="title"
        self.app_name="app_name"
        self.smw = SessionMainWindow(self.title, self.app_name)
        
    def test_removeTemp_when_current_session_folder_exists(self):
        try:
            self.smw.current_session_folder = "Test Session Folder"
            os.mkdir(self.smw.current_session_folder)
            self.smw.removeTemp()
            self.assertFalse(os.path.exists(self.smw.current_session_folder))
        except Exception as e:
            try:
                shutil.rmtree(self.smw.current_session_folder)
            except:
                pass
            raise e

    def test_removeTemp_when_current_session_folder_does_not_exist(self):
        self.smw.current_session_folder = "Test Session Folder"
        self.smw.removeTemp()

    def test_removeTemp_when_current_session_folder_exists_and_working_dir_is_it(self):
        try:
            self.smw.current_session_folder = "Test Session Folder"
            os.mkdir(self.smw.current_session_folder)
            os.chdir(self.smw.current_session_folder)
            self.smw.removeTemp()
        except Exception as e:
            try:
                os.chdir("..")
                shutil.rmtree(self.smw.current_session_folder)
            except:
                pass
            raise e

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

if __name__ == "__main__":
    unittest.main()



