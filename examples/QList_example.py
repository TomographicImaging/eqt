from PySide2 import QtCore, QtWidgets, QtGui
import glob, sys, os
from eqt.ui import UIFormFactory
from eqt.ui.UIFormWidget import FormWidget
from PySide2.QtWidgets import QListWidget
from PySide2.QtCore import Qt

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
        
        #pb.clicked.connect(lambda: self.openFormDialog())
        #qlist = createListWidget()
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(qlist)
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        self.show()

class ListWidgetWithDeleteButtons(QtWidgets.QListWidget):
    def __init__(self):
        QtWidgets.QListWidget.__init__(self)

        #self.setSortingEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)


    def addItems(self, items):
        for item_name in items:
            group_box = QtWidgets.QGroupBox()
            label = QtWidgets.QLabel(parent=group_box, text=item_name)
            # verticalLayout = QtWidgets.QHBoxLayout(self)
            # verticalLayout.addWidget(label)
            # verticalLayout.addWidget(QtWidgets.QPushButton("Delete!"))
            
            # group_box.setLayout(verticalLayout)

            form_widget = FormWidget()

            btn = QtWidgets.QPushButton()

            pixmapi = getattr(QtWidgets.QStyle, 'SP_DockWidgetCloseButton')
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)

            button = btn
            button.setMaximumSize(button.minimumSizeHint())
            form_widget.addWidget(button, label, item_name)
            item = QtWidgets.QListWidgetItem(self)
            item.setSizeHint(form_widget.sizeHint())
            self.addItem(item)
            self.setItemWidget(item, form_widget)
            #self.setItemWidget(item, group_box)
        # QtWidgets.QListWidget.addItems(self, items)
        # for i in range(self.count()):
        #     print(i)
        #     item = self.item(i)
        #     #self.setItemWidget(item, self.close_button)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    
    sys.exit(app.exec_())