from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class SequencesList(QWidget):
    def __init__(self, parent=None):
        super(SequencesList, self).__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        label = QLabel("List")
        layout.addWidget(label)
        self.setLayout(layout)