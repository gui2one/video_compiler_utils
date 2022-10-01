
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
    def H264(quality  : int = 10, output : str = "output.mp4"):
        print("H264 preset")
        args = [
                    f'-c:v', f'libx264', 
                    f'-preset', 'slow', 
                    f'-crf', f'{quality}' ,
                    f'-pix_fmt', f'yuv420p', 
                    f'-c:a', 'copy',
                    f'{output}'
                ]  
        return args
    
    def H265(quality  : int = 10, output : str = "output.mp4"):
        print("H265 preset")
        args = [
                    f'-c:v', f'libx265', 
                    f'-preset', 'slow', 
                    f'-crf', f'{quality}' ,
                    f'-pix_fmt', f'yuv420p',                
                    f'-c:a', 'copy',
                    f'{output}'
                ]  
        return args
    
    def ProRes(profile  : PRORES_profiles = PRORES_profiles.LT, output : str = "output.mp4"):
        
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
        
        
        print("ProRes preset")

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
                    f'-c:v', f'prores', 
                    f'-pix_fmt', f'{yuv_input}', 
                    f'-profile:v', f'{profile.value}', 
                    f'-quant_mat', f'{quant_mat.value}' ,
                    
                    f'-c:a', 'copy',
                    f'{output}'
                ]  
        return args