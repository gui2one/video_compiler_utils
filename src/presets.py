
from enum import Enum
import profile
class PRORES_profiles(Enum):
    PROXY = 0
    LT = 1
    STANDARD = 2
    HQ = 3
    prores4444 = 4
    prores4444XQ = 5
    
class PRORES_quant_mats(Enum):
    AUTO = 0
    DEFAULT = 1
    PROXY = 2
    LT = 3
    STANDARD = 4
    HQ = 5
class FFMpegPreset :
    
    @staticmethod
    def H264(quality  : int = 10):
        print("H264 preset")
        args = [
                    '-c:v', 'libx264', 
                    '-preset', 'slow', 
                    '-crf', f'{quality}' ,
                    '-pix_fmt', 'yuv420p', 
                    '-filter_complex', "color=black,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1",
                    '-c:a', 'copy'
                ]  
        return args
    
    def H265(quality  : int = 10):
        print("H265 preset")
        args = [
                    '-c:v', 'libx265', 
                    '-preset', 'slow', 
                    '-crf', f'{quality}' ,
                    '-pix_fmt', f'yuv420p',    
                    '-filter_complex', "color=black,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1",            
                    '-c:a', 'copy'
                ]  
        return args
    
    def ProRes(profile  : PRORES_profiles = PRORES_profiles.LT):
        
        """ from the docs
            profile -> integer
            

            0 : proxy
            1 : lt
            2 : standard
            3 : hq
            4 : 4444         not working !
            5 : 4444xq       not working !
            ----------------------------
            quant_mat integer


            0 : auto
            1 : default
            2 : proxy
            3 : lt
            4 : standard
            5 : hq
        """

        quant_mat : PRORES_quant_mats = None
        yuv_input = "yuv422p10"
        if profile == PRORES_profiles.PROXY :
            quant_mat = PRORES_quant_mats.PROXY
        elif profile == PRORES_profiles.LT : 
            quant_mat = PRORES_quant_mats.LT
        elif profile == PRORES_profiles.STANDARD : 
            quant_mat = PRORES_quant_mats.DEFAULT
        elif profile == PRORES_profiles.HQ : 
            quant_mat = PRORES_quant_mats.HQ
        elif profile == PRORES_profiles.prores4444 : 
            quant_mat = PRORES_quant_mats.HQ
            yuv_input = "yuv444p10"
        elif profile == PRORES_profiles.prores4444XQ : 
            quant_mat = PRORES_quant_mats.HQ
            yuv_input = "yuv444p10"
        args = [
                    '-c:v', 'prores', 
                    '-pix_fmt', f'{yuv_input}', 
                    '-profile:v', f'{profile.value}', 
                    '-quant_mat', f'{quant_mat.value}' ,
                    '-filter_complex', "color=black,format=rgb24[c];[c][0]scale2ref[c][i];[c][i]overlay=format=auto:shortest=1,setsar=1",
                    '-c:a', 'copy'
                ]  
        return args