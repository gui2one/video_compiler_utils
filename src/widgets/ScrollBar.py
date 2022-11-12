from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class ScrollBar(QScrollBar):
    def __init__(self, parent=None):
        super(ScrollBar, self).__init__(parent)
        self.setFixedWidth(10)
        
    def sizeHint(self) -> QSize:
        return QSize(10,10)
