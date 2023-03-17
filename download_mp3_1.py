import yt_dlp
import scrapetube
from tqdm import tqdm
import shutil
from hashlib import sha256
import os
from pathlib import Path

youtube_video_url = ''

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
    videos = scrapetube.get_channel(channel_id)
    
    counter = 0
    audioUrl_list =[]

    # Set options for downloading the audio file
    options = {
        'format': 'bestaudio/best',
        #'outtmpl': 'C:/users/jp/desktop/pinecone_project/final_pinecone_project/video',
        'outtmpl': '/notebooks/audio_files/video',
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
        youtube_video_url = 'https://www.youtube.com/watch?v='+ video['videoId']
        audioUrl_list.append('https://www.youtube.com/watch?v=' + video['videoId']) 
        

    #loop through each link in the file
    for audio in audioUrl_list:
        if limit == counter:
            print("limit reached")
            break

        filename = remove_backslash(audio)
        length = len(audioUrl_list)
        # Download the audio file
        ydl.download([audio])
        print(f"Video {counter} of {length} downloaded")
        os.rename('/notebooks/audio_files/video.mp3', f'/notebooks/audio_files/{filename}' + '.mp3')
        #os.rename('C:\\users\\jp\\desktop\\pinecone_project\\final_pinecone_project\\video.mp3', f'C:\\users\\jp\\desktop\\pinecone_project\\final_pinecone_project\\{filename}' + '.mp3')
       
        counter = counter + 1

    