from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

class SliderWidget(QWidget):
    
    
    value_changed = Signal(int)
    def __init__(self, label : str, default : int = 50, min : int = 0, max : int = 100, parent = None):
        super(SliderWidget, self).__init__(parent)
        
        self.label = label
        self.min = min
        self.max = max
        self.default = default
        
        self.initUI()
        
    def initUI(self):
        
        v_layout = QVBoxLayout()
        h_layout = QHBoxLayout()
        
        label = QLabel(self.label)
        v_layout.addWidget(label)
        
        v_layout.addLayout(h_layout)
        self.slider = QSlider()
        h_layout.addWidget(self.slider)
        
        self.int_value = QLabel("val")
        self.int_value.setText(str(self.default))
        h_layout.addWidget(self.int_value)
        self.slider.setOrientation(Qt.Orientation.Horizontal)
        self.slider.setValue(self.default)
        self.slider.setMinimum(self.min)
        self.slider.setMaximum(self.max)
        self.slider.valueChanged.connect(self.onChange)
        self.setLayout(v_layout)

    def onChange(self, value):
        self.int_value.setText(str(value))
        self.value_changed.emit(value)