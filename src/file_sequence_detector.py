
from genericpath import isdir, isfile
import re
import os
from typing import List
from logger import logger

from dataclasses import dataclass

@dataclass
class IFileSequence :
    num_files : int
    name_pattern : str
    start_number : int

class FileSequenceDetector :
    
    all_files : List[str]
    sequences : List[IFileSequence]
    
    def __init__(self, ):
        self.sequences = []
    
    def list_files(self, dir_path)->List[str]:
        if os.path.isdir(dir_path):
            all_files = os.listdir(dir_path)    
        return all_files  
    
    def detect_file_sequences(self, path : str):
        max_tries = 10
        num_tries = 0
        
        if os.path.isdir(path) :
            self.all_files = self.list_files(path)
        elif os.path.isfile(path):
            logger.info("this is a file. This is not possible at the moment ....")
            return

        while len(self.all_files):
            first_file = self.all_files[0]

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
                indices_to_delete = []
                for i, file in enumerate(self.all_files) :
                    r = re.compile(f'{parts[0]}\d+{parts[1]}')
                    ranges =[[m.start(),m.end()] for m in r.finditer(file)]
                    if len(ranges):
                        
                        num_files += 1
                        indices_to_delete.append(i)
                
                
                for i, file in reversed(list(enumerate(self.all_files))):
                    r = re.compile(f'{parts[0]}\d+{parts[1]}')
                    ranges =[[m.start(),m.end()] for m in r.finditer(file)]

                        
                def keep_function(item):
                    
                    parts = first_file.split(num_pattern)

                    if len(parts) < 2 : return True
                    r = re.compile(f'{parts[0]}\d+{parts[1]}')
                    ranges =[[m.start(),m.end()] for m in r.finditer(item)]            

                    return len(ranges) == 0
                
                filtered = filter(keep_function, self.all_files)
                
                self.all_files = list(filtered)
                                
                final_pattern = f'{parts[0]}%0{len(num_pattern)}d{parts[1]}'
                final_path = os.path.join(final_pattern)
                final_path = final_path.replace("\\", "/")
                
                result_sequence = IFileSequence(num_files, final_pattern, int(num_pattern) )


                self.sequences.append(result_sequence)
                
            num_tries += 1
            if num_tries > max_tries : break
            
    def print(self):
        if len(self.sequences) :
            for seq in self.sequences:
                print(seq)
        else : 
            print("No sequences ....")