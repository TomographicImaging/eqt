import sys
from PySide2 import QtGui, QtWidgets, QtCore


class CustomListWidgetItem(QtWidgets.QListWidgetItem, QtWidgets.QLabel):
    def __init__(self, parent=None):
        QtWidgets.QListWidgetItem.__init__(self, parent)
        QtWidgets.QLabel.__init__(self, parent)

class QCustomQWidget (QtWidgets.QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel    = QtWidgets.QLabel()
        self.textDownQLabel  = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QtWidgets.QHBoxLayout()
        self.iconQLabel      = QtWidgets.QLabel()
        self.allQHBoxLayout.addWidget(self.iconQLabel, 0)
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def setIcon (self, imagePath):
        self.iconQLabel.setPixmap(QtGui.QPixmap(imagePath))

class exampleQMainWindow (QtWidgets.QMainWindow):
    def __init__ (self):
        super(exampleQMainWindow, self).__init__()
        # Create QListWidget
        self.myQListWidget = QtWidgets.QListWidget(self)
        for index, name, icon in [
            ('No.1', 'Meyoko',  'icon.png'),
            ('No.2', 'Nyaruko', 'icon.png'),
            ('No.3', 'Louise',  'icon.png')]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQCustomQWidget.setIcon(icon)
            # Create QListWidgetItem
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        self.setCentralWidget(self.myQListWidget)

app = QtWidgets.QApplication([])
window = exampleQMainWindow()
window.show()
sys.exit(app.exec_())