import sys
from time import sleep

from PySide2 import QtCore, QtWidgets
from PySide2.QtCore import QThreadPool

from eqt.threading import Worker
from eqt.ui import ProgressTimerDialog
from eqt.ui.SessionDialogs import ErrorDialog


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Start Process")
        pb.clicked.connect(lambda: self.startProcess())

        pb2 = QtWidgets.QPushButton(self)
        pb2.setText("Start Process 2")
        pb2.clicked.connect(lambda: self.startProcessWithError())

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        layout.addWidget(pb2)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        self.threadpool = QThreadPool()

        self.show()

    def startProcess(self):
        process_name = "My example process"
        self.create_timer_progress_window(process_name)
        worker = Worker(self.example_process)
        worker.signals.finished.connect(self.progress_windows[process_name].close)
        self.threadpool.start(worker)

    def startProcessWithError(self):
        process_name = "My example process, with an error"
        self.create_timer_progress_window(process_name)
        worker = Worker(self.example_process_with_error)

        worker.signals.finished.connect(self.progress_windows[process_name].close)
        worker.signals.error.connect(self.process_error_dialog)
        self.threadpool.start(worker)

    def example_process(self, **kwargs):
        sleep(10)

    def example_process_with_error(self, **kwargs):
        sleep(3)
        raise Exception("Error!!")

    def process_error_dialog(self, error, **kwargs):
        dialog = ErrorDialog(self, "Error", str(error[1]), str(error[2]))
        dialog.open()

    def create_timer_progress_window(self, process_name):
        if not hasattr(self, 'progress_windows'):
            self.progress_windows = {}

        progress_window = ProgressTimerDialog(process_name, parent=self, flags=QtCore.Qt.Window)

        self.progress_windows[process_name] = progress_window
        progress_window.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
