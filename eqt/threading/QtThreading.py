# -*- coding: utf-8 -*-
"""
Basic classes for Threading a Qt application
Created on Wed Feb  6 11:10:36 2019

@author: ofn77899
"""

#https://www.geeksforgeeks.org/migrate-pyqt5-app-to-pyside2/
import traceback
import sys
from PySide2 import QtCore
from PySide2.QtCore import Slot

class Worker(QtCore.QRunnable):
    """Worker: defines a QRunnable to execute a function asynchronously. It handles worker thread setup, signals and wrapup."""
    
    def __init__(self, fn, *args, **kwargs):
        '''Worker creator
        
        :param fn: The function to be run by this Worker in a different thread. 
        :param args: positional arguments to pass to the function
        :param kwargs: keyword arguments to pass to the function
        
        The creator will add progress_callback, message_callback and status_callback to the kwargs.
        '''
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add progress callback to kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['message_callback'] = self.signals.message
        self.kwargs['status_callback'] = self.signals.status

    @Slot()
    def run(self):
        """
        Run the worker. Emits signals based on run state.
        Signals:
            - Error: Emitted when an exception is thrown in the workers function.
            - Result: Emitted if function completes successfully. Contains the return value of the function.
            - Finished: Emitted on completion of the worker thread.

        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()

class WorkerSignals(QtCore.QObject):
    """
    Defines signals available when running a worker thread
    Supported Signals:
    finished
        No Data

    error
        `tuple` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress
    
    message
        `string` with some text
    status
        `tuple` 
    """

    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    
    progress = QtCore.Signal(int)
    message = QtCore.Signal(str)
    status = QtCore.Signal(tuple)
