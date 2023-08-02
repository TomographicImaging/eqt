import sys

import qdarkstyle
from PySide2 import QtWidgets
from qdarkstyle.dark.palette import DarkPalette

from eqt.ui.ReOrderableListWidget import ReOrderableListWidget


class MainUI(QtWidgets.QMainWindow):
    def __init__(self, parent=None, title=None):
        QtWidgets.QMainWindow.__init__(self, parent)

        self.setWindowTitle(title)

        qlist = ReOrderableListWidget()
        qlist.addItems(["Transmission to Absorption", "Centre of Rotation Correction"])
        qlist.addItem("FBP")

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(qlist)
        layout.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)

        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        style = qdarkstyle.load_stylesheet(palette=DarkPalette)
        self.setStyleSheet(style)

        self.show()

        qlist.getItemNames()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    window = MainUI(title="ReOrderableListWidget")
    window.resize(400, 150)

    sys.exit(app.exec_())
