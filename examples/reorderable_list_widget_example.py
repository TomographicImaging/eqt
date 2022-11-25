from eqt.ui.ReOrderableListWidget import ReOrderableListWidget
from PySide6 import QtWidgets
import sys
try:
    import qdarkstyle
    from qdarkstyle.dark.palette import DarkPalette
    HAS_QDARKSTYLE = True
except:
    HAS_QDARKSTYLE = False

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None, title=None):
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

        if  HAS_QDARKSTYLE:
             style = qdarkstyle.load_stylesheet(palette=DarkPalette)
             self.setStyleSheet(style)

        self.show()

        qlist.getItemNames()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI(title="ReOrderableListWidget")
    window.resize(400, 150)
    
    sys.exit(app.exec_())