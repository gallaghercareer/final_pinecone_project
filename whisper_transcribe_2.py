import os
import shutil
import whisper
import json
import re
import torch

def add_backslash(url):
    url = url.replace('[', '/')
    url = url.replace(']', ':')
    url = url.replace("'", '?')
    return url

def get_segment_dict(result, url):
    segment_dict = {}
    url_without_extension = url[:-4]
    for segment in result['segments']:
        segment_dict[segment['id']] = {
            'url': url_without_extension,
            'start': segment['start'],
            'end': segment['end'],
            'text': segment['text'],
            'tokens': segment['tokens'],
            'temperature': segment['temperature'],
            'avg_logprob': segment['avg_logprob'],
            'compression_ratio': segment['compression_ratio'],
            'no_speech_prob': segment['no_speech_prob']
        }
    return segment_dict

def transcribe_mp3():
    print("beginning transcription script")
    devices = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
    model = whisper.load_model("medium" , device =devices)
    cwd = os.getcwd()
    

    with os.scandir(cwd) as entries:
        mp3_files = (entry for entry in entries if entry.is_file() and entry.name.endswith('.mp3'))
        list_mp3_files = list(mp3_files)
        total = len(list_mp3_files)        
        counter = 1
        
        for mp3_file in list_mp3_files:
                       
            print(f"transcribing {counter} of {total}")

            url = add_backslash(mp3_file.name)

            result = model.transcribe(mp3_file.path)
            print("file transcribed")

            filename = mp3_file.name[:-4] + ".txt"
            segment_dict = get_segment_dict(result, url)

            with open(filename, 'w') as file:
                file.write(str(segment_dict))

            shutil.move(filename, f'./{filename}')
            counter = counter + 1
    
    print("transcriptions COMPLETE")