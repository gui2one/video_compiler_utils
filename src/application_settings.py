from PySide2.QtCore import QSettings, QSize, QPoint

from logger import logger
from typing import Any
import os
import tempfile

class ApplicationSettings(QSettings):
    
    def __init__(self, scope : str = "gui2one_software", app_name : str = "Video Compiler Utils"):
        super(ApplicationSettings, self).__init__(scope,app_name)
        
        # self.applicationName() 
        self.initSettings()

    def initSettings(self):

        if not self.value("last_path"):
            self.setValue("last_path", "")        
      
        if not self.value("window_position"):
            self.setValue("window_position", QPoint(200,200))        
      
        if not self.value("window_size"):
            self.setValue("window_size", QSize(1280,720))        
      
        if not self.boolValue("window_maximized"):
            self.setValue("window_maximized", False)        
      
        if not self.value("h264__crf") :
            self.setValue("h264__crf", 15)
            
        if not self.value("h265__crf") :
            self.setValue("h265__crf", 15)

        if not self.value("global__fps") :
            self.setValue("global__fps", 25)

        if not self.value("database_path") :
            db_path = os.path.join(tempfile.gettempdir(), "vcu_database.db")
            self.setValue("database_path", str(db_path))
        
    def value(self, property_name : str) -> any:
        try :
            return super().value(property_name)
        except:
            logger.warning("value not found in settings")
            return None
        
    def boolValue(self, property_name) -> any :
        try :
            return super().value(property_name, type=bool)
        except Exception as e:
            logger.info(e)
            
    def setLastVisitedPath(self, path):
        self.setValue("last_path", path)
        
    def getLastVisitedPath(self):
        return self.value("last_path")

    def setWindowPosition(self, pos : QPoint):
        self.setValue("window_position", pos)

    def getWindowPosition(self):
        return self.value("window_position")

    def setWindowSize(self, size : QSize):
        self.setValue("window_size", size)
        
    def getWindowSize(self):
        return self.value("window_size")
    
    def getWindowMaximized(self):
        return self.boolValue("window_maximized")
    
    def setWindowMaximized(self, value : bool) :
        self.setValue("window_maximized", value)
        
    def setFFMPEGPath(self, path):
        self.setValue("ffmpeg_path", path)
        
    def getFFMPEGPath(self):
        return self.value("ffmpeg_path")    

    def setH264_CRF(self, path):
        self.setValue("h264__crf", path)
        
    def getH264_CRF(self):
        return self.value("h264__crf")    

    def setH265_CRF(self, path):
        self.setValue("h265__crf", path)
        
    def getH265_CRF(self):
        return self.value("h265__crf")    

    def setGlobal_FPS(self, value):
        self.setValue("global__fps", value)
        
    def getGlobal_FPS(self):
        return self.value("global__fps")    
    
    