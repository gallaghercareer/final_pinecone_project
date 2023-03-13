import os
import subprocess
import shutil
import whisper
import ffmpeg

#pip3 install ffmeg-python
#pip3 install numba
#pip3 install git+https://github.com/openai/whisper.git 
#pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
#sudo apt upgrade && sudo apt install ffmpeg
#pip3 install setuptools-rust
model = whisper.load_model("base")


def transcribe_mp3():
    #current working directory
    cwd = os.getcwd()
    print("outer reached")
	# Iterate through all files and directories in the input directory
    for file in os.listdir("."):   
        print("checking filename of files in directory tree")
        
        if file.endswith('.mp3'):        
            
            result = model.transcribe(file)

            # Define the path to the new directory
            #new_directory = os.path.join(".", "transcribed_text")

            # Create the new directory if it doesn't already exist

            #os.makedirs(new_directory, exist_ok=True)
            #print(result['text'])
            
            filename = file + ".txt"
            
            try:
                with open(filename, "w+") as f:
                    f.write(result['text'])
                    print("SUCCESS WRITTEN TO FILE")
            except Exception as e:
                print(f"Error writing to file: {e}")
            
            print("CLOSING FILE")
            f.close()
            shutil.move(filename, '/notebooks/transcribed')    
           # file_contents_path = file_contents.name
            
       
            
transcribe_mp3()