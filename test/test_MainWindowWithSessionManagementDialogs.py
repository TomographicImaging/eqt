import unittest
from unittest import mock

from eqt.ui.MainWindowWithSessionManagement import MainWindowWithSessionManagement
from eqt.ui.SessionDialogs import LoadSessionDialog

from . import skip_ci

# Unit tests for the MainWindowWithSessionManagement class
# methods which create dialogs


@skip_ci
class TestMainWindowWithSessionManagementCreateLoadSessionDialog(unittest.TestCase):
    '''
    Tests the createLoadSessionDialog method of the MainWindowWithSessionManagement class

    This method is responsible for creating the load session dialog
    and populating it with the available sessions
    '''
    def setUp(self):
        self.title = "title"
        self.app_name = "app_name"
        self.smw = MainWindowWithSessionManagement(self.title, self.app_name)
        self.smw.sessions_directory = mock.MagicMock()
        self.zip_folders = ["zip_folder_1", "zip_folder_2"]

    def test_createLoadSessionDialog_populates_session_dropdown(self):
        dialog = self.smw.createLoadSessionDialog(self.zip_folders)
        assert dialog is not None
        assert isinstance(dialog, LoadSessionDialog)
        select_session_combo = dialog.getWidget('select_session')
        assert select_session_combo is not None
        items_in_combo = [
            select_session_combo.itemText(i) for i in range(select_session_combo.count())]
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
