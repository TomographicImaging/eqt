import sys

import utilitiesForExamples
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
    advanced_dialog = AdvancedFormDialog(parent=parent, title='Example',
                                         parent_button_name='button_advanced')
    # all widgets
    utilitiesForExamples.addWidgetsToExample(advanced_dialog)
    for name in utilitiesForExamples.list_all_widgets():
        advanced_dialog.displayWidgetValueOnParent(name)
    # show
    parent.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    run_example()
    sys.exit(app.exec_())
