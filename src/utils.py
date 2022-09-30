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
                        abort = True
            self.message_event.emit(msg)
            
    def exit(self) -> None:
        # print("Thread EXIT")
        self.process.kill()
        return super().exit()            

def detectFileSequence(path) :
    is_a_directory = os.path.isdir(path)
    if is_a_directory == True:
        # print("this is a dir")
        
        ffmpeg_path = ApplicationSettings().getFFMPEGPath()
        files = os.listdir(path)

        
        # num = re.findall('\d+', files[0])
        mo = re.finditer('\d+', files[0])

        seqs = []
        for match in mo:
            # print(match)
            seqs.append((match.start(), match.end()))
            
        # print(seqs)
        start = seqs[len(seqs)-1][0]
        end   = seqs[len(seqs)-1][1]
        
        base = files[0]
        left_part = base[0: start]
        right_part = base[end: len(base)]
        
        length = end-start
        file_pattern = f'{left_part}%0{length}d{right_part}'

        
        final_path_string = os.path.join(path, file_pattern)
       
        
        final_path_string = final_path_string.replace("/", "\\") #.replace("/", "\\\\")

        dir_name = os.path.basename(path)
        
        output = os.path.join(os.path.dirname(path), f"{dir_name}.mp4")
        
        cmd = [
                f'{ffmpeg_path}/bin/ffmpeg', 
                '-y',
                f'-i', f'{final_path_string}',
                f'-pix_fmt', f'yuv420p', 
                f'-c:v', f'libx264', 
                f'-preset', 'slow', 
                f'-crf', f'10' ,
                f'-c:a', 'copy' ,
                f'{output}'
            ]       

        
        return cmd, len(files)

    else :
        print("this is a File")
        return None        
