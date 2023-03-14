import os
import subprocess
import shutil
import whisper
import ffmpeg
from hashlib import sha256

#pip3 install ffmeg-python
#pip3 install numba
#pip3 install git+https://github.com/openai/whisper.git 
#pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
#sudo apt upgrade && sudo apt install ffmpeg
#pip3 install setuptools-rust


def add_backslash(url):
        url =  input_str.replace('[', '/')
        url = input_str.replace(']',':')
        return url

def transcribe_mp3():
    
    model = whisper.load_model("base")
    #current working directory
    cwd = os.getcwd()
    print("outer reached")
	# Iterate through all files and directories in the input directory
    
    for file in os.listdir("."):   
        print("checking filename of files in directory tree")
        
        if file.endswith('.mp3'):        
            
            url = 
            result = model.transcribe(file)

            # Define the path to the new directory
            #new_directory = os.path.join(".", "transcribed_text")

            # Create the new directory if it doesn't already exist

            #os.makedirs(new_directory, exist_ok=True)
            #print(result['text'])
            
            print(result)
            filename = file + ".txt"
            
            data = file
            print(data)
            print(type(data))
            
            dictionary = [{}]
            try:
                with open(filename, "w+") as f:
                    for key, value in dictionary.items():
                        f.write(result['text'])
                        print("SUCCESS WRITTEN TO FILE")
            except Exception as e:
                print(f"Error writing to file: {e}")
            
            print("CLOSING FILE")
            f.close()
            shutil.move(filename, './transcribed')    
           # file_contents_path = file_contents.name
            
       
