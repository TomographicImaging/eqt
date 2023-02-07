from eqt.ui.SessionDialogs import WarningDialog, ErrorDialog, SaveSessionDialog, SessionDirectorySelectionDialog, LoadSessionDialog
import os
import unittest
from PySide2.QtWidgets import QApplication
import sys

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

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
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

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSaveSessionDialog(unittest.TestCase):
    def test_init(self):
        ssd = SaveSessionDialog()
        assert ssd is not None

    def test_init_with_title_param(self):
        title = "Test Save Session Dialog Title"
        ssd = SaveSessionDialog(title=title)
        self.assertEqual(ssd.windowTitle(), title)

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestSessionDirectorySelectionDialog(unittest.TestCase):
    def test_init(self):
        sdsd = SessionDirectorySelectionDialog()
        assert sdsd is not None

    def test_select_session_directory_label_when_app_name_not_set(self):
        sdsd = SessionDirectorySelectionDialog()

        self.assertEqual(sdsd.getWidget("select_session_directory").text(), "Select a session directory to save and retrieve all Sessions:")

    def test_select_session_directory_label_when_app_name_set(self):
        sdsd = SessionDirectorySelectionDialog(app_name="Test App")

        self.assertEqual(sdsd.getWidget("select_session_directory").text(), "Select a session directory to save and retrieve all Test App Sessions:")

    def test_browse_for_dir_button(self):
        sdsd = SessionDirectorySelectionDialog()
        # TODO: make test for this
        sdsd.browse_for_dir()

@unittest.skipIf(skip_as_conda_build, "On conda builds do not do any test with interfaces")
class TestLoadSessionDialog(unittest.TestCase):
    def test_init(self):
        lsd = LoadSessionDialog()
        assert lsd is not None

    def test_init_with_title_param(self):
        title = "Test Load Session Dialog Title"
        lsd = LoadSessionDialog(title=title)
        self.assertEqual(lsd.windowTitle(), title)



if __name__ == "__main__":
    unittest.main()