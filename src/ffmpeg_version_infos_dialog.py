from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from utils import get_ffmpeg_version

class FFMpegVersionInfosDialog(QDialog):
    def __init__(self, parent=None):
        super(FFMpegVersionInfosDialog, self).__init__(parent)
        self.setWindowTitle("FFmpeg Version Infos")
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        text_view = QTextEdit()
        text_view.setReadOnly(True)
        text_view.setText(f'{get_ffmpeg_version()}')
        layout.addWidget(text_view)