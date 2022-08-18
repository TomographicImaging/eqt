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
        
        #pb.clicked.connect(lambda: self.openFormDialog())
        #qlist = createListWidget()
        
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


    def addItems(self, items):
        for item_name in items:
            form_widget = QtWidgets.QWidget()

            verticalLayout = QtWidgets.QVBoxLayout(form_widget)

            # Add vertical layout to main widget (self)
            # verticalLayout.addWidget(self)
            form_widget.setLayout(verticalLayout)

            # Add group box
            groupBox = QtWidgets.QGroupBox(form_widget)

            # Add horizontal layout to group box
            layout = QtWidgets.QHBoxLayout(groupBox)

            # Add elements to layout
            verticalLayout.addWidget(groupBox)

            

            verticalLayout.setContentsMargins(1,0,1, 0)
            #print(form_widget.uiElements['verticalLayout'].setSpacing(100))
            label = QtWidgets.QLabel(groupBox, text=item_name) #parent=group_box,
            btn = QtWidgets.QPushButton()

            pixmapi = getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')   #DockWidgetCloseButton')
            icon = self.style().standardIcon(pixmapi)
            btn.setIcon(icon)

            button = btn
            button.setMaximumSize(button.minimumSizeHint())
            layout.addWidget(label)
            layout.addWidget(button )
            #layout.setWidget(button)#, alignment=QtCore.Qt.AlignRight)
            layout.setContentsMargins(2,2,2,2)
            # form_widget.uiElements['groupBoxFormLayout'].setFormAlignment(QtCore.Qt.AlignRight)
            #label.setAlignment(QtCore.Qt.AlignRight)
            
            
            item = QtWidgets.QListWidgetItem(self)
            print(form_widget.sizeHint())
            item.setSizeHint(form_widget.sizeHint()+ QtCore.QSize(5, 10))
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