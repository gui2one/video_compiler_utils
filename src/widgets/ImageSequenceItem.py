from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

import json
import os
from logger import logger
class ImageSequenceItem(QFrame):
    id : int
    time_stamp : float
    root_dir : str
    file_pattern : str
    
    deleted = Signal(int)
    def __init__(self, root_dir : str, file_pattern : str, id : int, parent=None):
        super(ImageSequenceItem, self).__init__(parent)
        self.setObjectName("ImageSequenceItem")
        self.root_dir = root_dir
        self.file_pattern = file_pattern
        self.id = id
        self.initUI()
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)


    def initUI(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        
        info_layout = QVBoxLayout()
        main_layout.addLayout(info_layout)
        
        title_label = QLabel(f'<span style="font-weight:bold;">{os.path.basename(self.root_dir)}</span>')
        title_label.setObjectName("title")
        info_layout.addWidget(title_label)
        hbox1 = QHBoxLayout()
        info_layout.addLayout(hbox1)
        
        dir_label = QLabel('Directory :')
        dir_label.setFixedWidth(60)
        dir_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        hbox1.addWidget(dir_label)
        
        dir_label2 = QLabel(f'<span style="font-weight:bold;">{self.root_dir}</span>')
        hbox1.addWidget(dir_label2)
        
        hbox2 = QHBoxLayout()
        info_layout.addLayout(hbox2)
        pattern_label = QLabel('Pattern :')
        pattern_label.setFixedWidth(60)
        pattern_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)
        hbox2.addWidget(pattern_label)
        pattern_label2 = QLabel(f'<span style="font-weight:bold;">{self.file_pattern}</span>')
        hbox2.addWidget(pattern_label2)
        
        delete_btn = QPushButton()
        delete_btn.setObjectName("delete_btn")
        # delete_btn.setStyleSheet("QPushButton{ border : 0px;}")
        pixmap = QPixmap("src/icons/trash_icon.png")
        delete_icon = QIcon(pixmap)
        delete_btn.setFixedSize(32,32)
        delete_btn.setIcon(delete_icon)
        delete_btn.setIconSize(delete_btn.size() * 0.8)
        delete_btn.clicked.connect(self.onDeletBtnClick)
        main_layout.addWidget(delete_btn, 0, alignment=Qt.AlignRight)
        
    def toJSON(self):
        data = {
            "root_dir" : self.root_dir,
            "file_pattern" : self.file_pattern
        }
        return json.dumps(data, indent=1)
        
    def fromJSON(self, json_data : dict):
        self.root_dir = json_data["root_dir"]
        self.file_pattern = json_data["file_pattern"]
        pass
    
    def onDeletBtnClick(self):
        logger.info(self.id, "-> from ImageSeq Item")
        self.deleted.emit(self.id)