from sqlite3 import connect
from PySide2 import QtCore, QtWidgets
import glob, sys, os
from eqt.ui import UIFormFactory, ProgressTimerDialog
from functools import partial
from PySide2.QtCore import QProcess
from PySide2.QtWidgets import (QAction, QComboBox, QDockWidget, QFileDialog,
                               QLabel, QMainWindow, QMenu, QMessageBox,
                               QProgressDialog, QStackedWidget, QTabWidget)

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        pb = QtWidgets.QPushButton(self)
        pb.setText("Start Process With Error")
        pb.clicked.connect(lambda: self.startProcessWithError())

        pb1 = QtWidgets.QPushButton(self)
        pb1.setText("Start Process With Warning")
        pb1.clicked.connect(self.startProcessWithWarning)

        pb2 = QtWidgets.QPushButton(self)
        pb2.setText("Start Process With Success")
        pb2.clicked.connect(lambda: self.startProcessWithSuccess())
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
        layout.addWidget(pb1)
        layout.addWidget(pb2)

        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        
    
    def startProcessWithError(self):
        command = "python " + r"/home/laura/Work/qt-tests/error_script.py"
        self.start_process(command, 'error_process')

    def startProcessWithWarning(self):
        command = "python " + r"/home/laura/Work/qt-tests/warning_script.py"
        self.start_process(command, 'warning_process')
    
    def startProcessWithSuccess(self):
        command = "python " + r"/home/laura/Work/qt-tests/successful_script.py"
        self.start_process(command, 'successful_process')

    def start_process(self, command, process_name, finish_connection=None,  error_connection=None, progress_known=False):
        self.process_finished = False
        if progress_known:
            self.create_progress_window(process_name, "Running {}".format(process_name), 
                    "Running {}".format(process_name), 100#"{}".format(command), 100 #,
                    #lambda: self.onCancel(process)
                    )
        else:
            self.create_unknown_progress_window(process_name)

        process = QProcess()
        self.process_failed = False
        if finish_connection is not None:
            process.finished.connect(lambda: self.process_finish_connection(process, process_name, finish_connection))
        else:
            process.finished.connect(self.progress_windows[process_name].close)
        if error_connection is not None:
            process.errorOccurred.connect(error_connection)
        else:
            self.error_printed_already = False
            process.errorOccurred.connect(partial(self.update_progress_error, process, process_name))
        if progress_known:
            process.readyReadStandardOutput.connect(lambda: self.update_progress(process, process_name))
        process.readyReadStandardError.connect(lambda: self.update_progress_error(process, process_name))

        process.start(command)

    def create_unknown_progress_window(self, process_name, title=None, detailed_text=None):

        progress_window = ProgressTimerDialog(process_name, parent=self)
        self.save_reference_to_progress_window(progress_window, process_name)
        progress_window.show()

    def save_reference_to_progress_window(self, progress_window, process_name):
        if not hasattr(self, 'progress_windows'):
            self.progress_windows = {}
        self.progress_windows[process_name] = progress_window

    def update_progress_error(self, process, process_name, error=None):
        if self.process_failed:
            # if process has already failed it means an error has already
            # been printed.
            return
        error_message = process.readAllStandardError()
        if error_message is not None:
            string = error_message
            line = str(string, "utf-8")
            #print("Error message is not None: ", line)
            
        else:
            line = str(error) + process.errorString()
            #print("Error Message was none, but now it is: ", line)

        useful_error_message_present = 'Exception' in line
        error_present = 'Exception' in line or ('Traceback' in line)

        if line == "":
            #print("The line is empty")
            return

        elif error_present:
            if useful_error_message_present:
                self.process_failed = True
                    
                if hasattr(self, 'progress_windows'):
                    self.progress_windows[process_name].close()
                process.kill()
                message = "An error occurred with: {}".format(process_name)
            else:
                return

        else:
            message = "A warning occurred in: {}".format(process_name)
        
        self.warningDialog(message, window_title=process_name, detailed_text=line)
        sys.stdout.flush()
            
        

    def warningDialog(self, message='', window_title='', detailed_text=''):
        # move to eqt MainWindow
        dialog = QMessageBox(self)
        dialog.setIcon(QMessageBox.Information)
        dialog.setText(message)
        dialog.setWindowTitle(window_title)
        dialog.setDetailedText(detailed_text)
        dialog.setStandardButtons(QMessageBox.Ok)
        retval = dialog.exec_()
        return retval

    def process_finish_connection(self, process, process_name, connection):
        self.process_finished = True
        self.progress_windows[process_name].close()
        if not self.process_failed and connection is not None:
            connection()
        
        
        

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    window.show()
    
    sys.exit(app.exec_())