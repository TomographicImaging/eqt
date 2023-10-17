import sys

from PySide2 import QtWidgets

from eqt.ui import UIFormWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        dock=UIFormWidget.FormDockWidget(parent=self)
        dock.setWindowTitle('Example remove widget')
        
        # add widget 1 as QLineEdit
        qlabel = QtWidgets.QLabel(dock)
        qlabel.setText("Widget 1: ")
        qwidget = QtWidgets.QLineEdit(dock)
        qwidget.setClearButtonEnabled(True)
        dock.addWidget(qwidget, qlabel, 'Widget 1')

        # add widget 2 as QLineEdit
        qlabel = QtWidgets.QLabel(dock)
        qlabel.setText("Widget 2: ")
        qwidget = QtWidgets.QLineEdit(dock)
        qwidget.setClearButtonEnabled(True)
        dock.addWidget(qwidget, qlabel, 'Widget 2')

        # add widget 3 as QLineEdit
        qlabel = QtWidgets.QLabel(dock)
        qlabel.setText("Widget 3: ")
        qwidget = QtWidgets.QLineEdit(dock)
        qwidget.setClearButtonEnabled(True)
        dock.addWidget(qwidget, qlabel, 'Widget 3')

        # add input as QComboBox
        dock.widget().addSpanningWidget(QtWidgets.QLabel("Pick the widget you want to remove: "), 'input_title')
        qlabel = QtWidgets.QLabel(dock)
        qlabel.setText("User input: ")
        qwidget = QtWidgets.QComboBox(dock)
        qwidget.addItem("Widget 2")
        qwidget.addItem("Widget 3")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        dock.addWidget(qwidget, qlabel, 'userinput')

        # add a button to remove widget 1
        buttonremove = QtWidgets.QPushButton(dock)
        buttonremove.setText("Remove widget 1")
        dock.widget().addSpanningWidget(buttonremove,'Button Remove')
        buttonremove.clicked.connect(lambda: self.remove(dock,'Widget 1'))

        # add a button to remove user selected widget 
        buttonremove = QtWidgets.QPushButton(dock)
        buttonremove.setText("Remove user selected widget")
        dock.widget().addSpanningWidget(buttonremove,'Button Remove User')
        buttonremove.clicked.connect(lambda: self.remove(dock))

        # add a button to remove spanning widget
        buttonremove = QtWidgets.QPushButton(dock)
        buttonremove.setText("Remove spanning widget")
        dock.widget().addSpanningWidget(buttonremove,'Button Remove Spanning')
        buttonremove.clicked.connect(lambda: self.remove(dock,'input_title'))

        # print dictionary of all widgets
        print("Dictionary of widgets:\n" +str(dock.widget().getWidgets()))
        
        self.show()

    def remove(self,dock,userselection=False):
        if userselection is False:
            userselection=dock.getWidget('userinput').currentText()
        print("Remove "+userselection)
        dock.removeWidget(userselection)
        print("Dictionary of widgets after deletion of "+userselection+":\n" +str(dock.widget().getWidgets()))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
