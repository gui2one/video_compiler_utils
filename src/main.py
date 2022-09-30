from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from application_settings import ApplicationSettings
from options_dialog import OptionsDialog

from utils import detectFileSequence, FFMPEG_thread
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

        if event.mimeData().hasUrls() :
            url :QUrl = event.mimeData().urls()[0]
            good_path = url.toLocalFile()

            cmd, num_frames = detectFileSequence(good_path)

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