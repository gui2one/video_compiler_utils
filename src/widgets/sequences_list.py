from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from widgets.ImageSequenceItem  import ImageSequenceItem 
import data_base
from logger import logger
class SequencesList(QWidget):
    
    sequences : list[ImageSequenceItem]
    
    updated = Signal()
    def __init__(self, parent=None):
        super(SequencesList, self).__init__(parent)
        self.setObjectName("SequenceList")
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.MinimumExpanding)

        self.initUI()
        
        
    def initUI(self):
        self.layout = QVBoxLayout()
        # self.layout.setContentsMargins(0,0,0,0)
        self.sequences = data_base.readItems()
        
        for seq in self.sequences :
            self.layout.addWidget(seq)
            seq.deleted.connect(self.onDeleteItem)
            
        if len(self.sequences) == 0 :
            label = QLabel("No Sequences")
            self.layout.addWidget(label)
        
        self.setLayout(self.layout)
        self.update()
    
    def onDeleteItem(self, id : int):
        data_base.deleteItem(id)
        logger.info(id, "-> from ImageSeq List")
        self.updated.emit()
        