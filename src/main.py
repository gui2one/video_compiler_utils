import os
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
from options_dialog import OptionsDialog

from presets import FFMpegPreset, PRORES_profiles
from utils import detect_file_sequence_V2, detectFileSequence, FFMPEG_thread
class MainWindow(QMainWindow) :
   
    def __init__(self) -> None:
        super(MainWindow, self).__init__()
        
        self.setGeometry(800,200, 512, 512)
        self.setWindowTitle("Video Compiler Utils")
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
        
        self.text_area = QTextEdit()
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
            pattern, num_frames = detect_file_sequence_V2(good_path)
            # cmd = [
            #         f'{ffmpeg_path}/bin/ffmpeg', 
            #         '-y',
            #         '-apply_trc', 'iec61966_2_1', # automatic gamma correction even with exrs !!
            #         f'-i', f'{pattern}',
            #         f'-pix_fmt', f'yuv420p', 
            #         f'-c:v', f'libx264', 
            #         f'-preset', 'slow', 
            #         f'-crf', f'10' ,
                    
            #         f'-c:a', 'copy',
            #         f'{output}'
            #     ]    
            cmd = [
                    f'{ffmpeg_path}/bin/ffmpeg', 
                    '-y',
                    '-apply_trc', 'iec61966_2_1', # automatic gamma correction even with exrs !!
                    f'-i', f'{pattern}',

                    
                    # *FFMpegPreset.H265(output=output+".mp4")
                    *FFMpegPreset.ProRes(profile=PRORES_profiles.PROXY,output=output+".mov")
                    
                ]    
            
            # FFMpegPreset.H264()

            self.ffmpeg_thread = FFMPEG_thread(cmd, num_frames)
            self.ffmpeg_thread.message_event.connect(self.on_ffmpeg_thread_message)
            self.ffmpeg_thread.start()
            
    def on_ffmpeg_thread_message(self, message):  
        self.text_area.append(message.strip())   
    
app = QApplication([])

with open("src/style.qss", "r") as file:
    app.setStyleSheet(file.read())
    pass

main_app = MainWindow()
app.exec_()