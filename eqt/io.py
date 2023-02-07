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

        # Could potentially be used for reporting progress:
        # total_size = 0
        # for dirpath, dirnames, filenames in os.walk(directory):
        #     for f in filenames:
        #         fp = os.path.join(dirpath, f)
        #         total_size += os.path.getsize(fp)

        if compress:
            compress_type = zipfile.ZIP_DEFLATED
        else:
            compress_type = zipfile.ZIP_STORED

        for r, d, f in os.walk(directory):
            for _file in f:
                fname = os.path.join(r, _file)
                zip.write(fname, _file, compress_type=compress_type)
                # Could potentially be used for reporting progress:
                #progress_callback.emit(os.path.getsize(fname)/total_size)
        zip.close() 