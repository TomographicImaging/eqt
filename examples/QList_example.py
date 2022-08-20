from PySide2 import QtCore, QtWidgets, QtGui
import glob, sys, os
from eqt.ui import UIFormFactory
from eqt.ui.UIFormWidget import FormWidget
from PySide2.QtWidgets import QListWidget
from PySide2.QtCore import Qt
try:
    import qdarkstyle
    from qdarkstyle.dark.palette import DarkPalette
    HAS_QDARKSTYLE = True
except:
    HAS_QDARKSTYLE = False

def createListWidget():
    listWidget = QListWidget()
    w, h = 15, 15
    scroll_size = 16
    listWidget.setFixedWidth(w + scroll_size)
    listWidget.setAttribute(Qt.WA_MacShowFocusRect, False)
    for x in range(10, 15):
        h = max(x + 1 * 2.0, h)
        pixmap = QtGui.QPixmap(w, h)
        pixmap.fill(Qt.transparent)
        painter = QtGui.QPainter(pixmap)
        center = h / 2.0
        painter.fillRect(QtCore.QRectF(1, center - x / 2.0,
                                w - 1 * 2.0, x), Qt.black)
        painter.end()
        label = QtWidgets.QLabel()
        label.setPixmap(pixmap)
        item = QtWidgets.QListWidgetItem(listWidget)
        item.setSizeHint(QtCore.QSize(w, h))
        item.setData(Qt.UserRole, x)
        listWidget.addItem(item)
        listWidget.setItemWidget(item, label)
        # if self._size == x:
        #     listWidget.setCurrentItem(item)
    return listWidget

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        qlist = ListWidgetWithDeleteButtons()
        qlist.addItems(["Transmission to Absorption", "Centre of Rotation Correction", "Beam Profile Correction"])
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(qlist)
        
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        if  HAS_QDARKSTYLE:
             style = qdarkstyle.load_stylesheet(palette=DarkPalette)
             self.setStyleSheet(style)

        self.show()

class ListWidgetWithDeleteButtons(QtWidgets.QListWidget):
    def __init__(self):
        QtWidgets.QListWidget.__init__(self)

        #self.setSortingEnabled(True)
        #self.setStyleSheet("QListWidget {margin: 0px;} QListWidget::item { padding: 0px; }")
        self.setSpacing(0)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.setDefaultDropAction(Qt.MoveAction)

        self.close_buttons = {}
        self.items = {}

    def addItems(self, items):
        for item_name in items:
            print(item_name)
            form_widget = QtWidgets.QWidget()

            verticalLayout = QtWidgets.QVBoxLayout(form_widget)
            # Add vertical layout to main widget
            form_widget.setLayout(verticalLayout)
            # Add group box
            groupBox = QtWidgets.QGroupBox(form_widget)
            # Add horizontal layout to group box
            layout = QtWidgets.QHBoxLayout(groupBox)
            # Add elements to layout
            verticalLayout.addWidget(groupBox)

            verticalLayout.setContentsMargins(1, 0, 1, 0)
            label = QtWidgets.QLabel(groupBox, text=item_name)
            

            self.close_buttons[item_name] = QtWidgets.QPushButton()

            pixmapi = getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')
            icon = self.style().standardIcon(pixmapi)
            self.close_buttons[item_name].setIcon(icon)


            self.close_buttons[item_name].setMaximumSize(self.close_buttons[item_name].minimumSizeHint())
            layout.addWidget(label)
            layout.addWidget(self.close_buttons[item_name])
            layout.setContentsMargins(2,2,2,2)
            
            item = QtWidgets.QListWidgetItem(self)
            item.setSizeHint(form_widget.sizeHint() + QtCore.QSize(5, 10))
            self.addItem(item)
            self.setItemWidget(item, form_widget)
            self.items[item_name] = item

        for item_name in items:
            self.close_buttons[item_name].clicked.connect(lambda:self.on_button_clicked(item_name))

    def on_button_clicked(self, item_name):
        self.takeItem(self.indexFromItem(self.items[item_name]).row())
        del self.items[item_name]

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    
    sys.exit(app.exec_())