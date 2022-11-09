from PySide2 import QtCore, QtWidgets

class ReOrderableListWidget(QtWidgets.QTableWidget):      
    def __init__(self,parent=None):
        super(ReOrderableListWidget,self).__init__(parent)
        self.setColumnCount(1)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setDefaultSectionSize(35)
        self.horizontalHeader().setStretchLastSection(True)
        self.resizeColumnsToContents()
        
    def addItem(self, name):
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
        button.setProperty("name", name + "_delete")
        pixmapi = getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')
        icon = self.style().standardIcon(pixmapi)
        button.setIcon(icon)
        button.clicked.connect(self.onClickDelete)
        button.setMaximumSize(button.minimumSizeHint())
        verticalLayout.setContentsMargins(1, -0.9, 1, -0.9)
        layout.setContentsMargins(2,1,2,1)

        layout.addWidget(QtWidgets.QLabel(name))

        # Up and down buttons:
        button_up=QtWidgets.QPushButton()
        button_up.setProperty("name", name + "_up")
        pixmapi = getattr(QtWidgets.QStyle, 'SP_ArrowUp')
        icon = self.style().standardIcon(pixmapi)
        button_up.setIcon(icon)
        button_up.clicked.connect(self.onClickUp)
        button_up.setMaximumSize(button_up.minimumSizeHint())

        button_down=QtWidgets.QPushButton()
        button_down.setProperty("name", name + "_down")
        pixmapi = getattr(QtWidgets.QStyle, 'SP_ArrowDown')
        icon = self.style().standardIcon(pixmapi)
        button_down.setIcon(icon)
        button_down.clicked.connect(self.onClickDown)
        button_down.setMaximumSize(button_down.minimumSizeHint())

        layout.addWidget(button_up)
        layout.addWidget(button_down)
        layout.addWidget(button)
        
        self.setCellWidget(row,0,form_widget)

        item = QtWidgets.QTableWidgetItem(name)
        #text in column 1
        self.setItem(row,0,item)

    def addItems(self, names):
        for name in names:
            self.addItem(name)

    def onClickDelete(self):
        # find the item with the same name to get the row
        text=self.sender().property("name")
        item=self.findItems(text.replace("_delete", ""), QtCore.Qt.MatchExactly)[0]
        self.removeRow(item.row())

    def onClickUp(self):
        # find the item with the same name to get the row
        text=self.sender().property("name")
        item=self.findItems(text.strip("_up"),QtCore.Qt.MatchExactly)[0]
        current_row = item.row()
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

    def onClickDown(self):
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

    
    def getItemNames(self):
        text_list = []
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            text_list.append(item.text())
        return text_list

class ReOrderableListDockWidget(QtWidgets.QDockWidget):
    def __init__(self, parent=None):
        super(ReOrderableListDockWidget, self).__init__(parent)
        # Make a vertical layout
        self.setWidget(ReOrderableListWidget())