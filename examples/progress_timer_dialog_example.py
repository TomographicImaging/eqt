from PySide2 import QtCore, QtWidgets
import glob, sys, os
from eqt.ui import UIFormFactory
from eqt.ui.progress_timer_dialog import ProgressTimerDialog
from eqt.threading import Worker
from time import sleep
from PySide2.QtCore import QProcess, QRegExp, QSettings, Qt, QThreadPool
from PySide2.QtGui import QCloseEvent, QKeySequence, QRegExpValidator
from PySide2.QtWidgets import (QAction, QComboBox, QDockWidget, QFileDialog,
                               QLabel, QMainWindow, QMenu, QMessageBox,
                               QProgressDialog, QStackedWidget, QTabWidget)

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        pb = QtWidgets.QPushButton(self)
        pb.setText("Start Process")
        pb.clicked.connect(lambda: self.startProcess())
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(pb)
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

    def example_process(self, **kwargs):
        sleep(10)

    def create_timer_progress_window(self, process_name):
        if not hasattr(self, 'progress_windows'):
            self.progress_windows = {}

        progress_window = ProgressTimerDialog(process_name, parent=self, flags=QtCore.Qt.Window)

        self.progress_windows[process_name] = progress_window
        progress_window.show()


    def accepted(self):
        print ("accepted")
        print (self.fw.widgets['input1_field'].text())
        print (self.fw.widgets['input2_field'].currentText())
        
        self.dialog.close()

    def rejected(self):
        print ("rejected")
        self.dialog.close()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    
    sys.exit(app.exec_())