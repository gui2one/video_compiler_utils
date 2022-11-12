from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from widgets.ScrollBar import ScrollBar
class ScrollArea(QScrollArea):
    
    resized = Signal(QSize)
    def __init__(self, parent=None):
        super(ScrollArea, self).__init__(parent)

        self.setVerticalScrollBar(ScrollBar())

    def resizeEvent(self, arg__1: QResizeEvent) -> None:
        self.resized.emit(self.size())
        return super().resizeEvent(arg__1)

