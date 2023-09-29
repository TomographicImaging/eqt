import os
import zipfile


def zip_directory(directory: str, compress: bool = True):
    """
    Zips a directory, optionally compressing it.

    Parameters
    ----------
    directory
        The directory to be zipped.
    compress
        Whether to compress the directory.
    """
    compress_type = zipfile.ZIP_DEFLATED if compress else zipfile.ZIP_STORED
    with zipfile.ZipFile(f'{directory}.zip', 'a') as zipper:
        for r, _, f in os.walk(directory):
            for _file in f:
                filepath = os.path.join(r, _file)
                arcname = os.path.relpath(filepath, directory)
                zipper.write(filepath, arcname, compress_type=compress_type)
