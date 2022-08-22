import sys
from PySide2 import QtGui,QtCore, QtWidgets
try:
    import qdarkstyle
    from qdarkstyle.dark.palette import DarkPalette
    HAS_QDARKSTYLE = True
except:
    HAS_QDARKSTYLE = False

class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        qlist = myTable()
        #qlist.addItems(["Transmission to Absorption", "Centre of Rotation Correction", "Beam Profile Correction"])

        qlist.add_item("Transmission to Absorption")
        qlist.add_item("Centre of Rotation Correction")
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(qlist)
        
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        if  HAS_QDARKSTYLE:
             style = qdarkstyle.load_stylesheet(palette=DarkPalette)
             self.setStyleSheet(style)

        #self.setStyleSheet('QTableView::item{background:black;} QTableView{gridline-color:black;}')
        


        self.show()

class myTable(QtWidgets.QTableWidget):      
    def __init__(self,parent=None):
        super(myTable,self).__init__(parent)
        self.setColumnCount(1)
        self.setColumnWidth(0, self.width())
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(35)

    def add_item(self,name):
        #new row
        row=self.rowCount()
        self.insertRow(row)

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


        #button in column 0
        button=QtWidgets.QPushButton()
        button.setProperty("name",name + "_delete")
        pixmapi = getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')
        icon = self.style().standardIcon(pixmapi)
        button.setIcon(icon)
        button.clicked.connect(self.on_click_delete)
        button.setMaximumSize(button.minimumSizeHint())
        verticalLayout.setContentsMargins(0, -0.9, 0, -0.9)
        layout.setContentsMargins(2,0,2,0)

        layout.addWidget(QtWidgets.QLabel(name))

        

        # Up and down buttons:
        button_up=QtWidgets.QPushButton()
        button_up.setProperty("name", name + "_up")
        pixmapi = getattr(QtWidgets.QStyle, 'SP_ArrowUp')
        icon = self.style().standardIcon(pixmapi)
        button_up.setIcon(icon)
        button_up.clicked.connect(self.on_click_up)
        button_up.setMaximumSize(button_up.minimumSizeHint())

        button_down=QtWidgets.QPushButton()
        button_down.setProperty("name", name + "_down")
        pixmapi = getattr(QtWidgets.QStyle, 'SP_ArrowDown')
        icon = self.style().standardIcon(pixmapi)
        button_down.setIcon(icon)
        button_down.clicked.connect(self.on_click_down)
        button_down.setMaximumSize(button_down.minimumSizeHint())

        #form_widget.setSizeHint(form_widget.sizeHint() + QtCore.QSize(5, 10))
        layout.addWidget(button_up)
        layout.addWidget(button_down)
        layout.addWidget(button)
        
        self.setCellWidget(row,0,form_widget)

        item = QtWidgets.QTableWidgetItem(name)
        #item.setSizeHint(form_widget.sizeHint() + QtCore.QSize(0, 200))


        #text in column 1
        self.setItem(row,0,item)

    def on_click_delete(self):
        # find the item with the same name to get the row
        text=self.sender().property("name")
        item=self.findItems(text.strip("_delete"),QtCore.Qt.MatchExactly)[0]
        print("Button click at row:",item.row())
        self.removeRow(item.row())

    def on_click_up(self):
        # find the item with the same name to get the row
        text=self.sender().property("name")
        item=self.findItems(text.strip("_up"),QtCore.Qt.MatchExactly)[0]
        print("Button click at row:",item.row())
        current_row = item.row()
        print("The current row: ", current_row)
        if item.row() <= 0 or item.row() > (self.rowCount()-1):
            pass
        else:
            new_row = current_row - 1
            item_to_move_up = self.takeItem(current_row, 0)
            widget_to_move_up = self.cellWidget(current_row, 0)
            self.insertRow(new_row)
            self.setItem(new_row, 0, item_to_move_up)
            self.setCellWidget(new_row,0, widget_to_move_up)
            self.removeRow(current_row+1)
        

    def on_click_down(self):
        # find the item with the same name to get the row
        text=self.sender().property("name")
        item=self.findItems(text.replace("_down", ""),QtCore.Qt.MatchExactly)[0]
        current_row = item.row()

        if item.row() < 0 or item.row() >= self.rowCount()-1:
            pass
        else:
            new_row = current_row + 2
            item_to_move_up = self.takeItem(current_row, 0)
            widget_to_move_up = self.cellWidget(current_row, 0)
            self.insertRow(new_row)
            self.setItem(new_row, 0, item_to_move_up)
            self.setCellWidget(new_row,0, widget_to_move_up)
            self.removeRow(current_row)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    
    sys.exit(app.exec_())