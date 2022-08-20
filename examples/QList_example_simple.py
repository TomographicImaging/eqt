from PySide2 import QtCore, QtWidgets, QtGui
import sys


class MainUI(QtWidgets.QMainWindow):

    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
        
        qlist = ListWidgetWithDeleteButtons()
        qlist.addItems(["Item 1", "Item 2", "Item3"])
        
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(qlist)

        widg = QtWidgets.QWidget()
        widg.setLayout(layout)
        self.setCentralWidget(widg)

        self.show()



        

class ListWidgetWithDeleteButtons(QtWidgets.QListView):
    def __init__(self):
        QtWidgets.QListView.__init__(self)

        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)

        self.close_buttons = {}

        self.model = QtGui.QStandardItemModel(self)
        self.setModel(self.model)


    def addItems(self, items):
        for item_name in items:
            form_widget = QtWidgets.QWidget()

            #verticalLayout = QtWidgets.QVBoxLayout(form_widget)
            # Add vertical layout to main widget
            # form_widget.setLayout(verticalLayout)
            # # Add group box
            # groupBox = QtWidgets.QGroupBox(form_widget)
            # Add horizontal layout to group box
            layout = QtWidgets.QHBoxLayout(form_widget)
            form_widget.setLayout(layout)
            # # Add elements to layout
            # verticalLayout.addWidget(groupBox)
            
            self.close_buttons[item_name] = QtWidgets.QPushButton("x")

            self.close_buttons[item_name].setMaximumSize(self.close_buttons[item_name].minimumSizeHint())
            # layout.addWidget(label)
            layout.addWidget(self.close_buttons[item_name], alignment=QtCore.Qt.AlignRight)
            layout.setContentsMargins(2,2,2,2)
            
            # item = QtWidgets.QListWidgetItem(self)


            #self.close_buttons[item_name].clicked.connect(lambda:self.on_button_clicked(item))

            item = QtGui.QStandardItem(item_name)
            item.setSizeHint(form_widget.sizeHint() + QtCore.QSize(5, 10))
            self.model.appendRow(item)
            self.setIndexWidget(item.index(), form_widget)

    def on_button_clicked(self, item):
        self.removeItemWidget(item)
        del item

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    window = MainUI()
    
    sys.exit(app.exec_())