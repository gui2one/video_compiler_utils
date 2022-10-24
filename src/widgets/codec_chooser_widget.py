from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class CodecChooser(QWidget):
    changed = Signal(int)
    def __init__(self, parent = None):
        super(CodecChooser, self).__init__(parent)
        self.setObjectName("codec_chooser")
        self.initUI()
    def initUI(self):
        layout = QHBoxLayout()
        
        label = QLabel("Codec :")
        layout.addWidget(label)
        
        self.combo = QComboBox()
        self.combo.addItem("H264")
        self.combo.addItem("H265")
        self.combo.addItem("ProRes")
        layout.addWidget(self.combo)
        
        
        self.combo.currentIndexChanged.connect(lambda idx : self.changed.emit(idx))
        self.setLayout(layout)


    def getCurrentIndex(self):
        return self.combo.currentIndex()