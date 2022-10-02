import os
from typing import Text
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
from options_dialog import OptionsDialog
from text_output_window import TextOutputWidget
from presets import FFMpegPreset, PRORES_profiles
from utils import detect_file_sequence_V2, FFMPEG_thread, FFMPEG_thread_V2, ffmpeg_input_params, ffmpeg_output_params
class MainWindow(QMainWindow) :
   
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.setGeometry(800,200, 512, 512)
        self.setWindowTitle("VCU - Video Compiler Utils - v0.0.1a")
        self.window = Window(self)
        self.setCentralWidget(self.window)
        self.options_dialog = OptionsDialog()

        
        option_menu = self.menuBar().addMenu("Option")
        
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
    ffmpeg_thread : FFMPEG_thread
    ffmpeg_thread_2 : FFMPEG_thread_V2
    # text_output : TextOutputWidget
    def __init__(self, parent) :
        super(Window, self).__init__(parent=parent)

        self.settings = ApplicationSettings()


        self.setAcceptDrops(True)

        
        self.initUI()
        

        last_path = self.settings.getLastVisitedPath()
        
        print(last_path)
        
    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        label = QLabel("Drop a folder Here")
        label.setScaledContents(True)
        label.setObjectName("drop_label")
        layout.addWidget(label,alignment=Qt.AlignCenter)
        
        self.text_area = TextOutputWidget()
        self.text_area.setTextInteractionFlags(Qt.LinksAccessibleByMouse)
        self.text_area.setReadOnly(True)
        self.text_area.setAcceptRichText(True)
        layout.addWidget(self.text_area)        
        
    def dragEnterEvent(self, event):

        event.acceptProposedAction()
        
    def dropEvent(self, event):

        ffmpeg_path = self.settings.getFFMPEGPath()
        if event.mimeData().hasUrls() :
            url :QUrl = event.mimeData().urls()[0]
            good_path = url.toLocalFile()
            dir_name = os.path.basename(good_path)
            output = os.path.join(os.path.dirname(good_path), f"{dir_name}")
            pattern, start_frame, num_frames = detect_file_sequence_V2(good_path)
            
            print("pattern : --->", pattern)
            print("start_frame : --->", start_frame)
            print("num_frames : --->", num_frames)

            # cmd = [
            #         f'{ffmpeg_path}/bin/ffmpeg', 
            #         '-y',
            #         '-apply_trc', 'iec61966_2_1', # automatic gamma correction even with exrs !!
            #         f'-start_number', f'{start_frame}',
            #         f'-i', f'{pattern}',
                    
            #         # *FFMpegPreset.H264(output=output)
            #         *FFMpegPreset.ProRes(profile=PRORES_profiles.LT,output=output)
            # ]    

            # self.ffmpeg_thread = FFMPEG_thread(cmd, num_frames)
            # self.ffmpeg_thread.message_event.connect(self.on_ffmpeg_thread_message)
            # self.ffmpeg_thread.start()
            
            
            in_params = ffmpeg_input_params()
            in_params.pattern = pattern
            in_params.start_number = start_frame
            in_params.num_frames = num_frames
            
            out_params = ffmpeg_output_params()
            out_params.output_name = output+".mp4"
            out_params.vcodec = "libx264"
            
            self.ffmpeg_thread_2 = FFMPEG_thread_V2(in_params, out_params)
            self.ffmpeg_thread_2.message_event.connect(self.on_ffmpeg_thread_message_2)
            self.ffmpeg_thread_2.start()
            
    def on_ffmpeg_thread_message(self, message):  
        self.text_area.append(message.strip())   

    def on_ffmpeg_thread_message_2(self, message):  
        self.text_area.append(message.strip())   
    
app = QApplication([])

with open("src/style.qss", "r") as file:
    app.setStyleSheet(file.read())
    pass

main_app = MainWindow()
app.exec_()