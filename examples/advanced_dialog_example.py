import sys
from PySide2 import QtWidgets
from eqt.ui.FormDialog import AdvancedFormDialog
from eqt.ui.UIFormWidget import FormWidget

def run_example():
    parent = FormWidget(parent=None)
    # open advanced dialog button
    pb = QtWidgets.QPushButton(parent)
    pb.setText("Open Advanced Dialog")
    pb.clicked.connect(lambda: advanced_dialog.exec())
    parent.addSpanningWidget(pb, 'button_advanced')
    # extra button
    extra_button = QtWidgets.QPushButton(parent)
    extra_button.setText("Extra button")
    parent.addSpanningWidget(extra_button, 'extra_button')
    # create dialog
    advanced_dialog = AdvancedFormDialog(parent=parent, title='Example', parent_button_name='button_advanced')
    # widget 0
    advanced_dialog.insertWidget(0, 'input_title', QtWidgets.QLabel("Input Values: "))
    # widget 1
    qlabel = QtWidgets.QLabel(advanced_dialog.groupBox)
    qlabel.setText("Widget 1: ")
    qwidget = QtWidgets.QLineEdit(advanced_dialog.groupBox)
    advanced_dialog.insertWidget(1, 'widget1', qwidget, qlabel)
    # widget 2
    qlabel = QtWidgets.QLabel(advanced_dialog.groupBox)
    qlabel.setText("Widget 2: ")
    qwidget = QtWidgets.QComboBox(advanced_dialog.groupBox)
    qwidget.addItem("option A")
    qwidget.addItem("option B")
    qwidget.setCurrentIndex(0)
    qwidget.setEnabled(True)
    advanced_dialog.addWidget(qwidget, qlabel, 'widget2')
    # add to parent list
    advanced_dialog.displayWidgetValueOnParent('widget1')
    advanced_dialog.displayWidgetValueOnParent('widget2')
    # show
    parent.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    run_example()
    sys.exit(app.exec_())



