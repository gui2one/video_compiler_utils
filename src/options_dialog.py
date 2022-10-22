
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
from widgets.slider_widget import SliderWidget
class LineEdit(QLineEdit):
    
    def __init__(self, parent = None) :
        super(LineEdit, self).__init__(parent)

    
        
class OptionsDialog(QDialog):
    
    def __init__(self,parent = None):
        super(OptionsDialog, self).__init__(parent)
        self.settings = ApplicationSettings()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.option1 = LineEdit(self.settings.getFFMPEGPath())
        layout.addWidget(self.option1)
        
        self.option1.textChanged.connect(lambda value : self.settings.setFFMPEGPath(value))

        self.H264_quality = SliderWidget("H264 CRF (lower is better)", 31, 0, 61)
        self.H264_quality.value_changed.connect(self.onH264ValueChanged)
        
        layout.addWidget(self.H264_quality)

        self.setLayout(layout)        
        
    def onH264ValueChanged(self, value):
        self.settings.setH264Quality(value)