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
        button.setProperty("name",name)
        pixmapi = getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')
        icon = self.style().standardIcon(pixmapi)
        button.setIcon(icon)
        button.clicked.connect(self.on_click)
        button.setMaximumSize(button.minimumSizeHint())
        verticalLayout.setContentsMargins(0, 0, 0, 0)
        layout.setContentsMargins(2,0,2,0)

        layout.addWidget(QtWidgets.QLabel(name))

        layout.addWidget(button)

        #form_widget.setSizeHint(form_widget.sizeHint() + QtCore.QSize(5, 10))
        
        
        self.setCellWidget(row,0,form_widget)

        item = QtWidgets.QTableWidgetItem(name)
        item.setSizeHint(form_widget.sizeHint() + QtCore.QSize(5, 10))

        #text in column 1
        self.setItem(row,0,item)

    def on_click(self):
        # find the item with the same name to get the row
        text=self.sender().property("name")
        item=self.findItems(text,QtCore.Qt.MatchExactly)[0]
        print("Button click at row:",item.row())
        self.removeRow(item.row())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    
    sys.exit(app.exec_())