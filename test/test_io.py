import shutil

from pytest import fixture, mark

from eqt.io import zip_directory


@fixture
def test_file(tmp_path):
    """Create a zip file, which contains a session.json file"""
    subfile = tmp_path / "Test Subfolder" / "test_file.txt"
    subfolder = subfile.parent
    subfolder.mkdir(parents=True, exist_ok=True)
    subfile.write_text("test")
    return subfile


@mark.parametrize('compress', (True, False))
def test_zip_directory_compress_False(test_file, compress):
    folder = test_file.parent.parent
    zip_directory(folder, compress=compress)
    zipname = folder.with_suffix(".zip")
    assert zipname.is_file()
    shutil.unpack_archive(zipname, folder / "extracted")
    assert (folder / "extracted" / test_file.parts[-2] / test_file.parts[-1]).is_file()
