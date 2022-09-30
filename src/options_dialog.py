from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
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
        # self.option1.setValue(self.options.b_convert_png_to_jpeg)
        layout.addWidget(self.option1)
        
        self.option1.textChanged.connect(lambda value : self.settings.setFFMPEGPath(value))


        self.setLayout(layout)        