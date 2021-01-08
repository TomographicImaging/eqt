# -*- coding: utf-8 -*-
"""
Basic classes for Threading a Qt application
Created on Wed Feb  6 11:10:36 2019

@author: ofn77899
"""

#https://www.geeksforgeeks.org/migrate-pyqt5-app-to-pyside2/
from PySide2 import QtCore
import traceback
import sys
from PySide2.QtCore import QThreadPool

class Worker(QtCore.QRunnable):
    """
    Worker thread

    Inherits from QRunnable to handle worker thread setup, signals and wrapup.

    :param (function) callback:
        The function callback to run on this worker thread. Supplied
        args/kwargs will be pass to the runner.

    :param args:
        Arguments to pass to the callback function

    :param kwargs:
        Keyword arguments to pass to the callback function

    """
    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

        # Add progress callback to kwargs
        self.kwargs['progress_callback'] = self.signals.progress
        self.kwargs['message_callback'] = self.signals.message

    @QtCore.Slot()
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
    """

    finished = QtCore.Signal()
    error = QtCore.Signal(tuple)
    result = QtCore.Signal(object)
    progress = QtCore.Signal(int)
    message = QtCore.Signal(str)

class ErrorObserver:

   def __init__(self):
       self.__ErrorOccurred = False
       self.__ErrorMessage = None
       self.CallDataType = 'string0'

   def __call__(self, obj, event, message):
       self.__ErrorOccurred = True
       self.__ErrorMessage = message

   def ErrorOccurred(self):
       occ = self.__ErrorOccurred
       self.__ErrorOccurred = False
       return occ

   def ErrorMessage(self):
       return self.__ErrorMessage
