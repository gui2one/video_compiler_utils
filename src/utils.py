from ast import arg
from multiprocessing.connection import Pipe
import os
import re
import sys
from subprocess import DETACHED_PROCESS, Popen, PIPE, STDOUT, call, check_output


from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from application_settings import ApplicationSettings


from presets import FFMpegCodecParams

from logger import logger

class ffmpeg_input_params :
    pattern : str
    start_number : int
    num_frames : int
    
class ffmpeg_output_params :
    output_name : str
    vcodec : str

def get_ffmpeg_path():
    ffmpeg_dir = ""
    if getattr(sys, 'frozen', False):
        root_dir = os.path.dirname(sys.executable)
        ffmpeg_dir = os.path.join(root_dir, "3rd-party\\ffmpeg\\bin")
        

    # or a script file (e.g. `.py` / `.pyw`)
    elif __file__:
        root_dir = os.path.dirname(__file__)   
          
        ffmpeg_dir = os.path.abspath(os.path.join(root_dir, "..", "3rd-party\\ffmpeg\\bin"))

    return ffmpeg_dir

def get_ffmpeg_version() -> str:
    
    cmd = f'{get_ffmpeg_path()}/ffmpeg.exe -version'
    output = check_output(cmd)
    if output:
        return output.decode("utf-8")
    else : 
        return "couldn't find ffmpeg version ..."

class FFMPEG_thread(QThread):
    message_event = Signal(str)
    def __init__( self, input : ffmpeg_input_params, output : ffmpeg_output_params, args : list, parent = None ):
        
        super(FFMPEG_thread, self).__init__(parent)
        self.in_params = input
        self.out_params = output
        self.cmd_args = args
        self.settings = ApplicationSettings()
        
        
        
    def run(self):

        """ 
            bt709                        .D.V.... BT.709
            gamma                        .D.V.... gamma
            gamma22                      .D.V.... BT.470 M
            gamma28                      .D.V.... BT.470 BG
            smpte170m                    .D.V.... SMPTE 170 M
            smpte240m                    .D.V.... SMPTE 240 M
            linear                       .D.V.... Linear
            log                          .D.V.... Log
            log_sqrt                     .D.V.... Log square root
            iec61966_2_4                 .D.V.... IEC 61966-2-4
            bt1361                       .D.V.... BT.1361
            iec61966_2_1                 .D.V.... IEC 61966-2-1
            bt2020_10bit                 .D.V.... BT.2020 - 10 bit
            bt2020_12bit                 .D.V.... BT.2020 - 12 bit
            smpte2084                    .D.V.... SMPTE ST 2084
            smpte428_1                   .D.V.... SMPTE ST 428-1
        """
        
        global_fps = self.settings.getGlobal_FPS()
        process = Popen(
            [
                f"{get_ffmpeg_path()}/ffmpeg.exe", "-y",
                "-hide_banner", "-loglevel", "error", "-stats",
                "-apply_trc", "iec61966_2_1",
                "-start_number", f"{self.in_params.start_number}",
                "-r", f"{global_fps}", 
                "-i", self.in_params.pattern,
                *self.cmd_args, "-r", f"{global_fps}",
                self.out_params.output_name
            ], 
            creationflags=DETACHED_PROCESS,
            stdout=PIPE, stderr=PIPE)
        buf = bytearray()
        exit = False
        while not exit:
            c = process.stderr.read(1)

            if c == b'':
                break
            if c.decode('utf-8') == '\r':
                msg = buf.decode('utf-8')

                self.message_event.emit(msg)
                buf = bytearray()
            else :
                buf += c
        result_path = self.out_params.output_name.replace("\\", "/")
        self.message_event.emit("click to run ->")
        self.message_event.emit(" ")
        self.message_event.emit(f"<a style='color: white; font-weight:bold;' href='{result_path}'>{result_path}</a>")
        self.message_event.emit(" ")
        
    def exit(self) -> None:
        # logger.info("Thread EXIT")
        return super().exit()  
