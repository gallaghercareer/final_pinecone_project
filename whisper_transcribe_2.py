import os
import subprocess
import shutil
import whisper
import ffmpeg
from hashlib import sha256
import json
import torch
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
        return url

def transcribe_mp3():
    dictionary = [{}]
    

    devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
    model = whisper.load_model("medium" , device =devices)
    #current working directory
    cwd = os.getcwd()
    print("outer reached")
	# Iterate through all files and directories in the input directory
    
    for file in os.listdir("."):   
        print("checking filename of files in directory tree")
        
        if file.endswith('.mp3'):        
            
            url = add_backslash(file) 
            result = model.transcribe(file)
            
            print(result[text])
            filename = file + ".txt"
            

            dictionary = [{
            "text" : result['text'],
            "url" : url,
            'time' : result['start'],

            }]
            
            
            '''try:
                with open(filename, "w+") as f:
                    for key, value in dictionary.items():
                        f.write(result['text'])
                        print("SUCCESS WRITTEN TO FILE")
            except Exception as e:
                print(f"Error writing to file: {e}")
            
            print("CLOSING FILE")
            f.close()
            shutil.move(filename, './transcribed')  
            '''  
            #file_contents_path = file_contents.name
            
       
