
class FFMpegPreset :
    
    @staticmethod
    def H264(quality  : int = 10, output : str = "output.mp4"):
        print("H264 preset")
        args = [
                    f'-c:v', f'libx264', 
                    f'-preset', 'slow', 
                    f'-crf', f'{quality}' ,
                    
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
                    
                    f'-c:a', 'copy',
                    f'{output}'
                ]  
        return args
    
    def ProRes(quality  : int = 10, output : str = "output.mp4"):
        
        """ from the docs
            profile -> integer
            

            0 : proxy
            1 : lt
            2 : standard
            3 : hq
            4 : 4444
            5 : 4444xq
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

        args = [
                    f'-c:v', f'prores', 
                    f'-profile', '0', 
                    f'-quant_mat', f'0' ,
                    
                    f'-c:a', 'copy',
                    f'{output}'
                ]  
        return args