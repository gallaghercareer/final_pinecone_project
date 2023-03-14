import yt_dlp
import scrapetube
from tqdm import tqdm
import shutil
from hashlib import sha256
import os
from pathlib import Path


def remove_backslash(url):
    url = url.replace('/', '[')
    url = url.replace(':',']')
    url = url.replace('?',"'")
    return url

#Define a function to read in a single line file
def read_api_key(input_file):
    # Open the file in read mode
    with open(input_file, 'r') as file:
        # Read the contents of the file as a string
        string_variable = file.read()
        return string_variable

def download_mp3s(channel_id, limit=None):
    videos = scrapetube.get_channel(channel_id, limit)
    
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
        if limit == counter:
            print("limit reached")
            break

        filename = remove_backslash(audio)
       
        # Download the audio file
        ydl.download([audio])
        
        os.rename('C:\\mp3downloaded\\video.mp3', f'C:\\mp3downloaded\\{filename}' + '.mp3')
       
        counter = counter + 1

    