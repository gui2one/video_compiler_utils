from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class ConfirmDialog(QDialog):
    
    accept = Signal()
    def __init__(self, message : str, parent = None):
        super(ConfirmDialog, self).__init__(parent)
        self.message = message
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        question = QLabel(self.message)
        layout.addWidget(question)
        
        btn_box = QHBoxLayout()
        layout.addLayout(btn_box)
        
        btn_ok = QPushButton("OK")
        btn_box.addWidget(btn_ok)
        btn_ok.clicked.connect(self.onClickAccept)
        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.onClickCancel)
        btn_box.addWidget(btn_cancel)
        
        # self.show()
        
    def onClickAccept(self):
        self.accept.emit()
        self.close()
        
    def onClickCancel(self):
        self.close()