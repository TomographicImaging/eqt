from PySide2 import QtWidgets

def addWidgetsToExample(self,dialog):
    # add widget 1 as QLineEdit
    qlabel = QtWidgets.QLabel(dialog)
    qlabel.setText("Widget 1: ")
    qwidget = QtWidgets.QLineEdit(dialog)
    qwidget.setClearButtonEnabled(True)
    dialog.addWidget(qwidget, qlabel, 'Widget 1')

    # add widget 2 as QLineEdit
    qlabel = QtWidgets.QLabel(dialog)
    qlabel.setText("Widget 2: ")
    qwidget = QtWidgets.QLineEdit(dialog)
    qwidget.setClearButtonEnabled(True)
    dialog.addWidget(qwidget, qlabel, 'Widget 2')

    # add widget 3 as QLineEdit
    qlabel = QtWidgets.QLabel(dialog)
    qlabel.setText("Widget 3: ")
    qwidget = QtWidgets.QLineEdit(dialog)
    qwidget.setClearButtonEnabled(True)
    dialog.addWidget(qwidget, qlabel, 'Widget 3')

    # add input as QComboBox
    dialog.addSpanningWidget(
        QtWidgets.QLabel("Pick the widget you want to remove:"), 'input_title')
    qlabel = QtWidgets.QLabel(dialog)
    qlabel.setText("User input: ")
    qwidget = QtWidgets.QComboBox(dialog)
    qwidget.addItem("Widget 2")
    qwidget.addItem("Widget 3")
    qwidget.setCurrentIndex(0)
    qwidget.setEnabled(True)
    dialog.addWidget(qwidget, qlabel, 'userinput')

    # add a button to remove widget 1
    buttonremove = QtWidgets.QPushButton(dialog)
    buttonremove.setText("Remove widget 1")
    dialog.addSpanningWidget(buttonremove, 'Button Remove')
    buttonremove.clicked.connect(lambda: self.remove(dialog,'Widget 1'))

    # add a button to remove spanning widget
    buttonremove = QtWidgets.QPushButton(dialog)
    buttonremove.setText("Remove spanning widget")
    dialog.addSpanningWidget(buttonremove, 'Button Remove Spanning')
    buttonremove.clicked.connect(lambda: self.remove(dialog,'input_title'))

