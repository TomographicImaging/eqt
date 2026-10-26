"""
Basic classes for Threading a Qt application
Created on Wed Feb  6 11:10:36 2019
"""
import sys
import threading

# https://www.geeksforgeeks.org/migrate-pyqt5-app-to-pyside2
import traceback

from qtpy import QtCore
from qtpy.QtCore import Slot

# Workers are kept alive here until they are finished and pruned from the main thread.
# With autoDelete enabled, Qt destroys the QRunnable (and its WorkerSignals QObject) in the
# pool thread right after run() returns. With PySide6 this races with signal events still
# queued for the main thread and segfaults (seen on macOS).
_active_workers: "set[Worker]" = set()
_active_workers_lock = threading.Lock()


def _prune_finished_workers():
    with _active_workers_lock:
        finished = [w for w in _active_workers if w._done]
        for w in finished:
            _active_workers.discard(w)


class Worker(QtCore.QRunnable):
    """Executes a function asynchronously. Handles worker thread setup, signals, and wrapup."""
    def __init__(self, fn, *args, **kwargs):
        '''Worker creator

        :param fn: The function to be run by this Worker in a different thread.
        :param args: positional arguments to pass to the function
        :param kwargs: keyword arguments to pass to the function

        The creator will add progress_callback, message_callback and status_callback to the kwargs.
        '''
        super(Worker, self).__init__()

        # Python owns the lifetime of the worker, see _active_workers.
        self.setAutoDelete(False)
        self._done = False
        _prune_finished_workers()
        with _active_workers_lock:
            _active_workers.add(self)

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

        Signals
        -------
        - Error: An exception is thrown in the workers function.
        - Result: Contains the return value of a function that has just completed successfully.
        - Finished: Worker thread has completed.
        """
        try:
            result = self.fn(*self.args, **self.kwargs)
        except BaseException: # NOQA: B036
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()
            self._release_payload()

    def _release_payload(self):
        """Drop fn, args and kwargs (possibly large data) once the job is done.

        The empty Worker stays alive until pruned from the main thread, see _active_workers.
        """
        self.fn = None
        self.args = None
        self.kwargs = None
        self._done = True


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
