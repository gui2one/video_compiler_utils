from ast import arg
from multiprocessing.connection import Pipe
import os
import re
import sys
from subprocess import DETACHED_PROCESS, Popen, PIPE, STDOUT, call


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
    
def add_ffmpeg_to_path():

    ffmpeg_dir = ""
    if getattr(sys, 'frozen', False):
        root_dir = os.path.dirname(sys.executable)
        ffmpeg_dir = os.path.join(root_dir, "3rd-party\\ffmpeg\\bin")
        

    # or a script file (e.g. `.py` / `.pyw`)
    elif __file__:
        root_dir = os.path.dirname(__file__)   
          
        ffmpeg_dir = os.path.abspath(os.path.join(root_dir, "..", "3rd-party\\ffmpeg\\bin"))
        
    sys.path.append(ffmpeg_dir)
    logger.info(f'FFMPEG DIR : {ffmpeg_dir}')


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
class FFMPEG_thread_V2(QThread):
    message_event = Signal(str)
    def __init__( self, input : ffmpeg_input_params, output : ffmpeg_output_params, args : list, parent = None ):
        
        super(FFMPEG_thread_V2, self).__init__(parent)
        self.in_params = input
        self.out_params = output
        self.cmd_args = args
        
        
        
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
        
        process = Popen(
            [
                f"{get_ffmpeg_path()}/ffmpeg.exe", "-y",
                "-apply_trc", "iec61966_2_1",
                "-start_number", f"{self.in_params.start_number}",
                "-i", self.in_params.pattern,
                *self.cmd_args,
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
        # print("Thread EXIT")
        return super().exit()  
    
def detect_file_sequence(dir_path):
    if os.path.isdir(dir_path):
        all_files = os.listdir(dir_path)

        first_file = all_files[0]
        
        matches = re.findall(r'\d+', first_file)
        
        r = re.compile(r'\d+')
        ranges =[[m.start(),m.end()] for m in r.finditer(first_file)]
        
        assert len(matches) == len(ranges)
        
        num_pattern = None

        if len(ranges) :
            num_pattern = matches[len(matches)-1] # assume sequence numbers are the last numbers in file name 

            
        if num_pattern != None :
            
            parts = first_file.split(num_pattern)

            num_files = 0
            for file in all_files :
                r = re.compile(f'{parts[0]}\d+{parts[1]}')
                ranges =[[m.start(),m.end()] for m in r.finditer(file)]
                if len(ranges):
                    num_files += 1
            
            
            final_pattern = f'{parts[0]}%0{len(num_pattern)}d{parts[1]}'
            final_path = os.path.join(dir_path, final_pattern)
            final_path = final_path.replace("\\", "/")
            return final_path, int(num_pattern), num_files
        
        return None, None, None
        
    else :
        print("Not a dir")
        return None, None, None
        
