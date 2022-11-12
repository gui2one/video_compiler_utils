from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import json
class ImageSequenceItem(QFrame):
    root_dir : str
    file_pattern : str
    def __init__(self, parent=None):
        super(ImageSequenceItem, self).__init__(parent)
        self.setObjectName("ImageSequenceItem")
        self.root_dir = "C:/Fake/"
        self.file_pattern = "image.%04d.png"
        self.initUI()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        pass



    def initUI(self):

        layout = QVBoxLayout()
        
        self.setLayout(layout)
        dir_label = QLabel('Directory :')
        layout.addWidget(dir_label)
        dir_label2 = QLabel(f'{self.root_dir}')
        layout.addWidget(dir_label2)
        
    def toJSON(self):
        data = {
            "root_dir" : self.root_dir,
            "file_pattern" : self.file_pattern
        }
        return json.dumps(data, indent=1)
        
        pass