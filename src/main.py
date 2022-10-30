import os
import sys
from typing import Text
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
from options_dialog import OptionsDialog
from widgets.codec_chooser_widget import CodecChooser
from text_output_window import TextOutputWidget
from confirm_dialog import ConfirmDialog
from presets import FFMpegCodecParams, PRORES_profiles

from utils import (
    get_ffmpeg_path,
    detect_file_sequence, 
    FFMPEG_thread_V2, 
    ffmpeg_input_params, 
    ffmpeg_output_params
)

get_ffmpeg_path()
class MainWindow(QMainWindow) :
   
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        
        print(sys.path)
        
        self.setGeometry(500,200, 1024, 512)
        self.setWindowTitle("VCU - Video Compiler Utils - v0.0.1a")
        self.window = Window(self)
        self.setCentralWidget(self.window)
        self.options_dialog = OptionsDialog()

        
        option_menu = self.menuBar().addMenu("Options")
        
        action1 = QAction("display options", self)
        action1.triggered.connect(self.displayOptionsDialog)
        option_menu.addAction(action1)
        self.show()
        
    def closeEvent(self, event: QCloseEvent) -> None:

        return super().closeEvent(event)
    
    def displayOptionsDialog(self):
        self.options_dialog.exec_()
        pass
    
class Window(QWidget):

    ffmpeg_thread : FFMPEG_thread_V2
    # text_output : TextOutputWidget
    def __init__(self, parent) :
        super(Window, self).__init__(parent=parent)

        self.settings = ApplicationSettings()
        self.setAcceptDrops(True)
        self.initUI()


        
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        label = QLabel("Drop a folder Here")
        label.setScaledContents(True)
        label.setObjectName("drop_label")
        layout.addWidget(label,alignment=Qt.AlignCenter)
        
        self.chooser = CodecChooser()
        layout.addWidget(self.chooser,alignment=Qt.AlignRight)
        self.chooser.changed.connect(lambda x : print(x))

        self.text_area = TextOutputWidget()
        self.text_area.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.text_area.setReadOnly(True)
        self.text_area.setAcceptRichText(True)
        layout.addWidget(self.text_area)        
        
    def dragEnterEvent(self, event):

        event.acceptProposedAction()
        
    def dropEvent(self, event):

        # ffmpeg_path = self.settings.getFFMPEGPath()
        if event.mimeData().hasUrls() :
            url :QUrl = event.mimeData().urls()[0]
            good_path = url.toLocalFile()
            dir_name = os.path.basename(good_path)
            output = os.path.join(os.path.dirname(good_path), f"{dir_name}")
            pattern, start_frame, num_frames = detect_file_sequence(good_path)
            
            
            if pattern != None:

                self.in_params = ffmpeg_input_params()
                self.in_params.pattern = pattern
                self.in_params.start_number = start_frame
                self.in_params.num_frames = num_frames
                
                self.out_params = ffmpeg_output_params()
                
                self.cmd_args = []
                if self.chooser.getCurrentIndex() == 0 :
                    self.out_params.output_name = output+"_H264.mp4"
                    self.out_params.vcodec = "libx264"
                    self.cmd_args = FFMpegCodecParams.H264(quality=self.settings.getH264_CRF())
                elif self.chooser.getCurrentIndex() == 1 :
                    self.out_params.output_name = output+"_H265.mp4"
                    self.out_params.vcodec = "libx265"
                    self.cmd_args = FFMpegCodecParams.H265(quality=self.settings.getH265_CRF())
                elif self.chooser.getCurrentIndex() == 2 :
                    self.out_params.output_name = output+"_PRORES.mov"
                    self.out_params.vcodec = "prores"
                    self.cmd_args = FFMpegCodecParams.ProRes()
                 
                 
                if  os.path.exists(self.out_params.output_name) :            
                    name = os.path.basename(self.out_params.output_name)
                    diag = ConfirmDialog(f"<div style='font-size : 16px;'><span style='font-weight :bold;color:red;'>{name}</span> already exist in this directory.<br><br> Overwrite ?<div>", self)
                    diag.accept.connect(self.onAcceptOverwrite)
                    diag.exec_()  
                    
                else:
                    self.onAcceptOverwrite()
                             

            
    def on_ffmpeg_thread_message(self, message):  
        self.text_area.append(message.strip())   

    def on_ffmpeg_thread_message_2(self, message):  
        self.text_area.append(message.strip())   
        
    def onAcceptOverwrite(self):
        self.ffmpeg_thread = FFMPEG_thread_V2(self.in_params, self.out_params, self.cmd_args)
        self.ffmpeg_thread.message_event.connect(self.on_ffmpeg_thread_message_2)
        self.ffmpeg_thread.start()

app = QApplication([])

with open("src/style.qss", "r") as file:
    app.setStyleSheet(file.read())
    pass

main_app = MainWindow()
app.exec_()