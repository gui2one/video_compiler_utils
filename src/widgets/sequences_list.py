from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from widgets.ImageSequenceItem  import ImageSequenceItem 

class SequencesList(QFrame):
    
    sequences : list[ImageSequenceItem]
    def __init__(self, parent=None):
        super(SequencesList, self).__init__(parent)
        self.setObjectName("SequenceList")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)
        # self.setMinimumWidth(500)
        self.sequences = []
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        self.sequences.append(ImageSequenceItem())
        # self.sequences.append(ImageSequenceItem())
        # self.sequences.append(ImageSequenceItem())
        # self.sequences.append(ImageSequenceItem())
        # self.sequences.append(ImageSequenceItem())
        # self.sequences.append(ImageSequenceItem())
        self.initUI()
        
        
    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        for seq in self.sequences :
            layout.addWidget(seq)
        self.setLayout(layout)