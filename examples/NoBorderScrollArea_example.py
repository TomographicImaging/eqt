import sys

from PySide2 import QtWidgets
from PySide2.QtWidgets import QPushButton

from eqt.ui.NoBorderScrollArea import NoBorderScrollArea


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        """Any button added after the `NoBorderScrollArea` is instanced will not be styled as
        expected, due to the bug in `qdarkstyle`. The method `apply_qdarkstyle_to_buttons` needs
        to be invoked."""
        QtWidgets.QMainWindow.__init__(self, parent)

        layout = QtWidgets.QVBoxLayout()
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        layout.addWidget(QPushButton("Test"))
        layout.addWidget(QPushButton("Test2"))

        self.scroll_area_widget = NoBorderScrollArea(widg)

        layout.addWidget(QPushButton("Test3"))
        self.scroll_area_widget.apply_qdarkstyle_to_buttons(widg)
        layout.addWidget(QPushButton("Test4"))

        self.setCentralWidget(self.scroll_area_widget)

        self.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI()

    sys.exit(app.exec_())
