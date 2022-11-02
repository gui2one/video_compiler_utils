from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import json
class ImageSequenceItem(QWidget):
    root_dir : str
    file_pattern : str
    def __init__(self, parent=None):
        super(ImageSequenceItem, self).__init__(parent)
        self.root_dir = "C:/Fake/"
        self.file_pattern = "image.%04d.png"
        self.initUI()
        pass



    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        dir_label = QLabel('Root Directory :')
        layout.addWidget(dir_label)
        
    def toJSON(self):
        data = {
            "root_dir" : self.root_dir,
            "file_pattern" : self.file_pattern
        }
        return json.dumps(data, indent=1)
        
        pass