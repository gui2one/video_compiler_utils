from ctypes import alignment
import os
import sys
from typing import Text
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
from ffmpeg_version_infos_dialog import FFMpegVersionInfosDialog
from file_sequence_detector import FileSequenceDetector
from options_dialog import OptionsDialog
from widgets.codec_chooser_widget import CodecChooser
from text_output_window import TextOutputWidget
from confirm_dialog import ConfirmDialog
from presets import FFMpegCodecParams, PRORES_profiles

from utils import (
    FFMPEG_thread_V2, 
    ffmpeg_input_params, 
    ffmpeg_output_params
)
from widgets.int_param import IntParam


class MainWindow(QMainWindow) :
   
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.setGeometry(500,200, 1024, 512)
        self.setWindowTitle("VCU - Video Compiler Utils - v0.0.1a")
        
        self.setWindowIcon(QIcon("VCU_logo_01.ico"))        
        self.window = Window(self)
        self.setCentralWidget(self.window)
        self.options_dialog = OptionsDialog()
        self.ffmpeg_verion_infos_dialog = FFMpegVersionInfosDialog()

        
        misc_menu = self.menuBar().addMenu("Misc")
        
        action1 = QAction("display options", self)
        action1.triggered.connect(self.displayOptionsDialog)
        misc_menu.addAction(action1)
        action2 = QAction("ffmpeg version infos", self)
        action2.triggered.connect(self.displayFFMpegVersionInfos)
        misc_menu.addAction(action2)
        self.show()
        
    def closeEvent(self, event: QCloseEvent) -> None:

        return super().closeEvent(event)
    
    def displayOptionsDialog(self):
        self.options_dialog.exec_()
        pass
    
    def displayFFMpegVersionInfos(self):
        self.ffmpeg_verion_infos_dialog.exec_()
    
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
        
        hbox = QHBoxLayout()
        layout.addLayout(hbox)
        hbox.setSpacing(0)
        hbox.setAlignment(Qt.AlignRight)

        
        self.chooser = CodecChooser()
        self.chooser.setMaximumWidth(250)
        hbox.addWidget(self.chooser, 0, alignment=Qt.AlignRight)
        self.chooser.changed.connect(lambda x : print(x))
        
        
        rate_label = IntParam("fps", self.settings.getGlobal_FPS())
        rate_label.setMaximumWidth(100)
        rate_label.setObjectName("codec_chooser")
        rate_label.value_changed.connect(self.onRateChange)
        hbox.addWidget(rate_label, 0, alignment=Qt.AlignRight)        

        self.text_area = TextOutputWidget()
        self.text_area.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.text_area.setReadOnly(True)
        self.text_area.setAcceptRichText(True)
        layout.addWidget(self.text_area)        
        
    def dragEnterEvent(self, event):

        event.acceptProposedAction()
        
    def dropEvent(self, event):

        if event.mimeData().hasUrls() :
            
            detector = FileSequenceDetector()
            url :QUrl = event.mimeData().urls()[0]
            good_path = url.toLocalFile()
            dir_name = os.path.basename(good_path)
            output = os.path.join(os.path.dirname(good_path), f"{dir_name}")
            
            pattern = None
            start_frame = None
            num_frames = None

            
            detector.detect_file_sequences(good_path)
            detector.print()
            
            if len(detector.sequences) > 0 :
                seq = detector.sequences[0]
                pattern = os.path.join(good_path, seq.name_pattern)
                start_frame = seq.start_number
                num_frames = seq.num_files
            
            
            
            if pattern != None:

                self.in_params = ffmpeg_input_params()
                self.in_params.pattern = pattern
                self.in_params.start_number = start_frame
                self.in_params.num_frames = num_frames
                
                self.out_params = ffmpeg_output_params()
                
                fps = self.settings.getGlobal_FPS()
                self.cmd_args = []
                if self.chooser.getCurrentIndex() == 0 :
                    self.out_params.output_name = output+f"_H264_{fps}fps.mp4"
                    self.out_params.vcodec = "libx264"
                    self.cmd_args = FFMpegCodecParams.H264(quality=self.settings.getH264_CRF())
                elif self.chooser.getCurrentIndex() == 1 :
                    self.out_params.output_name = output+f"_H265_{fps}fps.mp4"
                    self.out_params.vcodec = "libx265"
                    self.cmd_args = FFMpegCodecParams.H265(quality=self.settings.getH265_CRF())
                elif self.chooser.getCurrentIndex() == 2 :
                    self.out_params.output_name = output+f"_PRORES_{fps}fps.mov"
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
        
    def onAcceptOverwrite(self):
        self.ffmpeg_thread = FFMPEG_thread_V2(self.in_params, self.out_params, self.cmd_args)
        self.ffmpeg_thread.message_event.connect(self.on_ffmpeg_thread_message)
        self.ffmpeg_thread.start()
        
    def onRateChange(self, value):
        print(value)
        self.settings.setGlobal_FPS(value)

app = QApplication([])

with open("src/style.qss", "r") as file:
    app.setStyleSheet(file.read())
    pass

main_app = MainWindow()
app.exec_()