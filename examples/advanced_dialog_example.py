import sys

from PySide2 import QtWidgets

from eqt.ui.FormDialog import AdvancedFormDialog
from eqt.ui.UIFormWidget import FormWidget


class FormExample(FormWidget):
    def __init__(self, parent=None):
        FormWidget.__init__(self, parent)

        pb = QtWidgets.QPushButton(self)
        pb.setText("Open Advanced Dialog with form layout")
        pb.clicked.connect(lambda: self.openFormDialog())
        self.addSpanningWidget(pb, 'buttadv')
        #dialog = AdvancedFormDialog(parent=self, title='Example')
        dialog = AdvancedFormDialog(parent=None, title='Example')
        
        dialog.Ok.clicked.connect(lambda: self.accepted())
        # Example on how to add elements to the FormDialog
        # add input 1 as QLineEdit
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Input 1: ")
        qwidget = QtWidgets.QLineEdit(dialog.groupBox)
        qwidget.setClearButtonEnabled(True)
        # finally add to the form widget
        dialog.insertWidgetToFormLayout(0, 'input_title', QtWidgets.QLabel("Input Values: "))
        dialog.insertWidgetToFormLayout(1, 'input1', qwidget, qlabel)
        dialog.addToDictionaryDisplayOnParent('input1')

        # add input 2 as QComboBox
        qlabel = QtWidgets.QLabel(dialog.groupBox)
        qlabel.setText("Input 2: ")
        qwidget = QtWidgets.QComboBox(dialog.groupBox)
        qwidget.addItem("option 1")
        qwidget.addItem("option 2")
        qwidget.setCurrentIndex(0)
        qwidget.setEnabled(True)
        # finally add to the form widget
        dialog.addWidget(qwidget, qlabel, 'input2')
        dialog.addToDictionaryDisplayOnParent('input2')
        print(dialog.getDisplayOnParentSet())
        dialog.addWidget(QtWidgets.QLabel("Example Vertical Layout Text"), layout="vertical")

        # store a reference
        self.dialog = dialog
        self.dialog.onCancel = self.rejected
        self.show()

    def openFormDialog(self):
        self.dialog.exec()

    def accepted(self):
        print(self.dialog.widgets['input1_field'].text())
        print(self.dialog.widgets['input2_field'].currentText())
        self.dialog.close()

    def rejected(self):
        print("rejected")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = FormExample()

    sys.exit(app.exec_())
