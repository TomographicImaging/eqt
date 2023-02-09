from eqt.io import zip_directory
import unittest
import os
import shutil

class TestZipDirectory(unittest.TestCase):

    def setUp(self):
        '''
        Create a session zip file, which contains a session.json file
        '''
        self.title="title"
        self.app_name="app_name"

        self.folder = "Test Folder"
        self.subfolder = os.path.join(self.folder, "Test Subfolder")
        self.subfile = os.path.join(self.subfolder, "test_file.txt")

        os.mkdir(self.folder)
        os.mkdir(self.subfolder)

        with open(self.subfile, "w+") as f:
            f.write("test")

    def test_zip_directory(self):
        zip_directory(self.folder)
        # Check the zip file exists:
        assert os.path.exists(self.folder + ".zip")
        # extract the zipfile and check the subfile exists:
        shutil.unpack_archive(self.folder + ".zip", "extracted")
        assert os.path.exists(os.path.join("extracted", "Test Subfolder", "test_file.txt"))

    def tearDown(self):
        shutil.rmtree(self.folder)


if __name__ == "__main__":
    unittest.main()