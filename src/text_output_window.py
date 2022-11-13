from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *


class TextOutputWidget(QTextEdit):
    
    def __init__(self, parent = None):
        super(TextOutputWidget, self).__init__(parent)
        self.setObjectName("text_area")
        
    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self.anchorAt(e.pos()):
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
        else:
            QApplication.restoreOverrideCursor()
        return super().mouseMoveEvent(e)
    
    def mousePressEvent(self, e):
        self.anchor = self.anchorAt(e.pos())
        if self.anchor:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def mouseReleaseEvent(self, e):
        if self.anchor:
            QDesktopServices.openUrl(QUrl(self.anchor))
            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.anchor = None
        
    def contextMenuEvent(self, e: QContextMenuEvent) -> None:
        menu = QMenu(self)
        action1 = QAction("clear all")
        action1.triggered.connect(lambda : self.clear())
        menu.addAction(action1)
        menu.addSection("hello")
        menu.exec_(e.globalPos())