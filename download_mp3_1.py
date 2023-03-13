import yt_dlp
import scrapetube
from tqdm import tqdm
import shutil
from hashlib import sha256
import os
from pathlib import Path



#Define a function to read in a single line file
def read_api_key(input_file):
    # Open the file in read mode
    with open(input_file, 'r') as file:
        # Read the contents of the file as a string
        string_variable = file.read()
        return string_variable

videos = scrapetube.get_channel("UCv83tO5cePwHMt1952IVVHw")
counter = 0
audioUrl_list =[]

# Set options for downloading the audio file
options = {
    'format': 'bestaudio/best',
    'outtmpl': 'C:/mp3downloaded/video',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }]
}

 # Create a yt-dlp object and pass in the options
ydl = yt_dlp.YoutubeDL(options)

for video in videos:
    #create list of video ids    
    audioUrl_list.append('https://www.youtube.com/watch?v=' + video['videoId']) 
    

#loop through each link in the file
for audio in audioUrl_list:
    total = len(audioUrl_list)
    print("Video downloaded and encoded, moving to {counter} of {total} in channel")
    hash = sha256(audio.encode()).hexdigest()[:13]    
    # Download the audio file
    ydl.download([audio])
    
    os.rename('C:\\mp3downloaded\\video.mp3', f'C:\\mp3downloaded\\{hash}' + '.mp3')
   
    counter = counter + 1

    