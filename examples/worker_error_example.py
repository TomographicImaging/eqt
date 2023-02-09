from PySide2 import QtCore, QtWidgets
import sys
from eqt.ui import ProgressTimerDialog
from eqt.threading import Worker
from time import sleep
from PySide2.QtCore import QThreadPool


class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        pb = QtWidgets.QPushButton(self)
        pb.setText("Start Process")
        pb.clicked.connect(self.startProcess)
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        self.threadpool = QThreadPool()

        self.show()
    
    def startProcess(self):
        process_name = "My example failing process"
        self.create_timer_progress_window(process_name)
        worker = Worker(self.example_failing_process)
        worker.signals.finished.connect(self.progress_windows[process_name].close)
        worker.signals.error.connect(self.open_error_dialog)
        self.threadpool.start(worker)

    def example_failing_process(self, **kwargs):
        sleep(2)
        raise Exception("This is an example exception")

    def open_error_dialog(self, error):
        error_dialog = QtWidgets.QMessageBox(self)
        error_dialog.setText(str(error[1]))
        error_dialog.setDetailedText(str(error[2]))
        error_dialog.open()

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