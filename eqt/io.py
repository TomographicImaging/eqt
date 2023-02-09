import os
import zipfile



def zip_directory(directory, compress=True, **kwargs):
        '''
        Zips a directory, optionally compressing it.
        
        Parameters
        ----------
        directory : str
            The directory to be zipped.
        compress : bool
            Whether to compress the directory.
        '''
        zip = zipfile.ZipFile(directory + '.zip', 'a')

        if compress:
            compress_type = zipfile.ZIP_DEFLATED
        else:
            compress_type = zipfile.ZIP_STORED

        for r, d, f in os.walk(directory):
            for _file in f:
                filepath = os.path.join(r, _file)
                arcname = os.path.relpath(filepath, directory)
                zip.write(filepath, arcname, compress_type=compress_type)
        zip.close() 