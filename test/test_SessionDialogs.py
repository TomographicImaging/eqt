import os
import unittest
from pathlib import Path
from unittest.mock import patch

from PySide2.QtWidgets import QFileDialog

from eqt.ui.SessionDialogs import (
    AppSettingsDialog,
    ErrorDialog,
    LoadSessionDialog,
    SaveSessionDialog,
    SessionDirectorySelectionDialog,
    WarningDialog,
)

from . import skip_ci


@skip_ci
class TestWarningDialog(unittest.TestCase):
    def test_init(self):
        wd = WarningDialog()
        assert wd is not None

    def test_init_with_params(self):
        message = "This is a test message"
        window_title = "Test Warning Dialog Title"
        detailed_text = "This is a test detailed text"

        wd = WarningDialog(message=message, window_title=window_title, detailed_text=detailed_text)
        self.assertEqual(wd.detailedText(), detailed_text)
        self.assertEqual(wd.text(), message)
        self.assertEqual(wd.windowTitle(), window_title)


@skip_ci
class TestErrorDialog(unittest.TestCase):
    def test_init(self):
        ed = ErrorDialog()
        assert ed is not None

    def test_init_with_params(self):
        message = "This is a test message"
        window_title = "Test Error Dialog Title"
        detailed_text = "This is a test detailed text"

        ed = ErrorDialog(message=message, window_title=window_title, detailed_text=detailed_text)
        self.assertEqual(ed.detailedText(), detailed_text)
        self.assertEqual(ed.text(), message)
        self.assertEqual(ed.windowTitle(), window_title)


@skip_ci
class TestSaveSessionDialog(unittest.TestCase):
    def test_init(self):
        ssd = SaveSessionDialog()
        assert ssd is not None

    def test_init_with_title_param(self):
        title = "Test Save Session Dialog Title"
        ssd = SaveSessionDialog(title=title)
        self.assertEqual(ssd.windowTitle(), title)


@skip_ci
class TestSessionDirectorySelectionDialog(unittest.TestCase):
    def test_init(self):
        sdsd = SessionDirectorySelectionDialog()
        assert sdsd is not None

    def test_select_session_directory_label_when_app_name_not_set(self):
        sdsd = SessionDirectorySelectionDialog()

        self.assertEqual(
            sdsd.getWidget("select_session_directory").text(),
            "Select a session directory to save and retrieve all Sessions:")

    def test_select_session_directory_label_when_app_name_set(self):
        sdsd = SessionDirectorySelectionDialog(app_name="Test App")

        self.assertEqual(
            sdsd.getWidget("select_session_directory").text(),
            "Select a session directory to save and retrieve all Test App Sessions:")

    @patch("PySide2.QtWidgets.QFileDialog.getExistingDirectory")
    def test_browse_for_dir_button_makes_file_dialog_for_getting_dir(self, mock_dialog_call):
        sdsd = SessionDirectorySelectionDialog()
        sdsd.browse_for_dir()
        mock_dialog_call.assert_called_once()

    @patch("PySide2.QtWidgets.QFileDialog.getExistingDirectory")
    def test_browse_button_calls_browse_for_dir(self, mock_dialog_call):
        sdsd = SessionDirectorySelectionDialog()
        sdsd.browse_for_dir = unittest.mock.Mock()
        QFileDialog.getExistingDirectory = unittest.mock.Mock()
        sdsd.getWidget("selected_dir").click()
        sdsd.browse_for_dir.assert_called_once()

    def test_browse_dialog_updates_session_directory_label(self):
        example_dir = "C:\\Users\\test_user\\Documents\\test_dir"
        sdsd = SessionDirectorySelectionDialog()
        QFileDialog.getExistingDirectory = unittest.mock.Mock()
        QFileDialog.getExistingDirectory.return_value = example_dir
        sdsd.browse_for_dir()
        self.assertEqual(
            sdsd.getWidget("selected_dir", "label").text(), os.path.basename(example_dir))

    def test_browse_dialog_updates_selected_dir_attribute(self):
        example_dir = "C:\\Users\\test_user\\Documents\\test_dir"
        sdsd = SessionDirectorySelectionDialog()
        QFileDialog.getExistingDirectory = unittest.mock.Mock()
        QFileDialog.getExistingDirectory.return_value = example_dir
        sdsd.browse_for_dir()
        self.assertEqual(sdsd.selected_dir, example_dir)


@skip_ci
class TestLoadSessionDialog(unittest.TestCase):
    def test_init(self):
        lsd = LoadSessionDialog()
        assert lsd is not None

    def test_init_with_title_param(self):
        title = "Test Load Session Dialog Title"
        lsd = LoadSessionDialog(title=title)
        self.assertEqual(lsd.windowTitle(), title)

    def test_init_with_location_of_session_files_param(self):
        location_of_session_files = Path("~").expanduser() / "some" / "test_dir"
        lsd = LoadSessionDialog(location_of_session_files=location_of_session_files)
        self.assertEqual(
            lsd.getWidget("sessions_directory").text(),
            f"Currently loading sessions from: {location_of_session_files}")


@skip_ci
class TestAppSettingsDialog(unittest.TestCase):
    def test_init(self):
        asd = AppSettingsDialog()
        assert asd is not None
