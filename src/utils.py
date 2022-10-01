import os
import re
import subprocess
from subprocess import Popen, PIPE, STDOUT
import sys
from typing import Tuple

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from application_settings import ApplicationSettings

import ffmpeg as ff

class ffmpeg_input_params :
    pattern : str
    start_number : int
    num_frames : int
    
class ffmpeg_output_params :
    output_name : str
    vcodec : str
    


class FFMPEG_thread_V2(QThread):
    message_event = Signal(str)
    def __init__( self, input : ffmpeg_input_params, output : ffmpeg_output_params, parent = None ):
        
        super(FFMPEG_thread_V2, self).__init__(parent)
        self.in_params = input
        self.out_params = output
        
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
        
        input = ff.input(
            self.in_params.pattern, 
            start_number = self.in_params.start_number,
            apply_trc ='iec61966_2_1',
            pix_fmt = 'yuv420p',
            filter_complex = "color=black,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1"
            )
        
        output = ff.output(
            input.video, 
            self.out_params.output_name, 
            vcodec=self.out_params.vcodec,
            
            ).overwrite_output()
        
        output.run()
        
        self.message_event.emit("DONE ?")
        
    def exit(self) -> None:
        print("Thread EXIT")
        # self.process.kill()
        return super().exit()  
    

class FFMPEG_thread(QThread):
    message_event = Signal(str)
    def __init__(self, cmd, num_frames, parent = None ):
        super(FFMPEG_thread, self).__init__(parent)
        self.cmd = cmd
        self.num_frames = num_frames


    def run(self):
        self.process = Popen( self.cmd, 
                stdout = PIPE, 
                stderr = STDOUT,
                shell = True)
        abort = False
        while not abort :
            line = self.process.stdout.readline()
            if not line : continue
            # print(f"got line : {line.decode('utf-8')}")
            msg = line.decode('utf-8').strip().replace("\n", "").replace("\r", "").strip()
            split = msg.split("frame= ")
            
            self.message_event.emit(msg)
            
            ## a little hacky, but it works for now:
            ## I just filter ffmpeg output lines and search for 'frame= ${num} blabla'
            ## when ${num} is equal to self.num_frames, abort ! work is done ....
            ## doesn't work if number of files in sequence doesn't equal number of files in directory !
            
            ## I NEED SOMETHING MORE ROBUST
            if len(split) > 1:    
                filtered = [item.strip() for item in split if len(item.strip())> 0]
                stripped = [item.strip() for item in filtered]
                numbers = [int(item.split(" ")[0]) for item in stripped]

                for num in numbers :
                    if num == self.num_frames:
                        self.exit()
                        # print(f"<span>[ INFO ] {message_str}</span>",  flush=True)
                        message_str = "Done"
                        self.message_event.emit(f"<span style='color:#228822;'>[ INFO ] {message_str}</span>")
                        abort = True
            
    def exit(self) -> None:
        print("Thread EXIT")
        self.process.kill()
        return super().exit()            

    
def detect_file_sequence_V2(dir_path):
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
                    # print(ranges)
                    # print(file)
                    num_files += 1
            
            
            final_pattern = f'{parts[0]}%0{len(num_pattern)}d{parts[1]}'
            final_path = os.path.join(dir_path, final_pattern)
            final_path = final_path.replace("\\", "/")
            return final_path, int(num_pattern), num_files
        
        return None
        
    else :
        print("Not a dir")
        return None
        
