import time
from time import sleep

from qtpy import QtCore
from qtpy.QtCore import Qt, QThreadPool
from qtpy.QtWidgets import QProgressDialog

from ..threading import Worker


class ProgressTimerDialog(QProgressDialog):
    def __init__(self, process_name, cancelText="Cancel", parent=None, flags=None,
                 cancel_method=None):
        if flags is None:
            flags = Qt.WindowFlags()
        labelText = f"Running {process_name}"
        QProgressDialog.__init__(self, labelText, cancelText, 0, 0, parent, flags)

        self.setWindowTitle(process_name)
        self.setMinimumDuration(0)
        # This means the other windows can't be used while this is open:
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMinimizeButtonHint, False)
        if cancel_method is None:
            self.setCancelButton(None)
        else:
            self.canceled.connect(cancel_method)

        self.threadpool = QThreadPool()
        self.process_name = process_name
        self.run_cancelled = False

    def update_progress_bar(self, value):
        self.setLabelText(f"Running {self.process_name} ... {value}s")

    def show(self):
        QProgressDialog.show(self)
        worker = Worker(self.timing_process)
        worker.signals.progress.connect(self.update_progress_bar)
        self.worker = worker
        self.threadpool.start(worker)

    def timing_process(self, **kwargs):
        progress_callback = kwargs.get('progress_callback')
        t0 = time.time()
        while not self.run_cancelled:
            progress_callback.emit(round(time.time() - t0))
            sleep(1)

    def close(self):
        # If we don't cause timing_process to stop
        # running then it continues forever,
        # even after the progress window closes.
        self.run_cancelled = True
        # need to wait for the thread to finish:
        self.threadpool.waitForDone()
        QProgressDialog.close(self)
