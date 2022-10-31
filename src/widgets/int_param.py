from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class IntParam(QWidget):
    
    value_changed = Signal(int)
    def __init__(self, label_str : str, value : int, parent=None):
        super(IntParam, self).__init__(parent)
        self.label_str = label_str
        self.value = value
        
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        label = QLabel(self.label_str)
        layout.addWidget(label)
        
        spin = QSpinBox()
        spin.setMaximum(250)
        layout.addWidget(spin)
        spin.valueChanged.connect(self.onValueChanged)
        
        spin.blockSignals(True)
        spin.setValue(self.value)
        spin.blockSignals(False)
        
        
        
    def onValueChanged(self, value):
        self.value_changed.emit(value)
