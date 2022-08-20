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

        qlist.add_item("kitten")
        qlist.add_item("unicorn")
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(qlist)
        
        widg = QtWidgets.QWidget()
        widg.setLayout(layout)

        self.setCentralWidget(widg)

        if  HAS_QDARKSTYLE:
             style = qdarkstyle.load_stylesheet(palette=DarkPalette)
             self.setStyleSheet(style)

        #self.setStyleSheet('QTableView::item{background:black;} QTableView{gridline-color:black;}')
        
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)

        self.show()

class myTable(QtWidgets.QTableWidget):      
    def __init__(self,parent=None):
        super(myTable,self).__init__(parent)
        self.setColumnCount(2)

    def add_item(self,name):
        #new row
        row=self.rowCount()
        self.insertRow(row)


        #button in column 0
        button=QtWidgets.QPushButton()
        button.setProperty("name",name)
        pixmapi = getattr(QtWidgets.QStyle, 'SP_DialogCancelButton')
        icon = self.style().standardIcon(pixmapi)
        button.setIcon(icon)
        button.clicked.connect(self.on_click)
        self.setCellWidget(row,1,button)

        #text in column 1
        self.setItem(row,0,QtWidgets.QTableWidgetItem(name))

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