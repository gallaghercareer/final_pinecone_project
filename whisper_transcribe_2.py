import os
import subprocess
import shutil
import whisper
import ffmpeg
from hashlib import sha256
import json
import torch
import download_mp3_1
import re

#pip3 install ffmeg-python
#pip3 install numba
#pip3 install git+https://github.com/openai/whisper.git 
#pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
#sudo apt upgrade && sudo apt install ffmpeg
#pip3 install setuptools-rust



def add_backslash(url):
        url =  url.replace('[', '/')
        url = url.replace(']',':')
        url = url.replace("'","?")
        url = url[:-4]
        return url

def transcribe_mp3():
   
    #devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
    #model = whisper.load_model("medium" , device =devices)
    
    model = whisper.load_model("base")
    #current working directory
    cwd = os.getcwd()
    print("outer reached")
    # Iterate through all files and directories in the input directory
    
    for file in os.listdir("."):   
        print("checking filename of files in directory tree")
        
        if file.endswith('.mp3'): 
            print(f"found file: {file}")
            url = add_backslash(file) 
            
            result = model.transcribe(file)
            
            print(result)
            filename = file + ".txt"
            
         
                
            segment_dict = {}
            for segment in result['segments']:
                segment_dict[segment['id']] = {
                    'url': url,
                    'start': segment['start'],
                    'end': segment['end'],
                    'text': segment['text'],
                    'tokens': segment['tokens'],
                    'temperature': segment['temperature'],
                    'avg_logprob': segment['avg_logprob'],
                    'compression_ratio': segment['compression_ratio'],
                    'no_speech_prob': segment['no_speech_prob']
                }
                
                
            with open(filename, 'w') as file:
                json.dump(segment_dict, file)
                file.close()

            shutil.move(filename, f'./{filename}')  
              
            
