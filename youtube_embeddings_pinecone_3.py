#pip3 install pinecone-client
#pip3 install openai
import scrapetube
from nltk.tokenize import sent_tokenize
from nltk.tokenize.punkt import PunktSentenceTokenizer
from nltk.tokenize import word_tokenize
import os
import openai
import numpy
import pinecone
from datasets import load_dataset
from datasets import get_dataset_split_names
from tqdm.auto import tqdm
from pprint import pprint
import json


# Define a function to split a list into chunks of a given size
def chunks(lst, size):
    return [lst[i:i+size] for i in range(0, len(lst), size)]

def embed_vectors(import_transcript):
    
    counter = 0
    
    #declare ID for all transcript snippets in Vector Database
    vector_batch_id = 0

    #declare vector total for increment
    vectorTotal = 0

    #vector list for every embedding
    vector_list = []


    joined_sentences = []
  
    with open(import_transcript, 'r') as file:
        segment_dict = json.load(file)    
    
    '''for segment_id, segment_data in segment_dict.items(): 
        
        
        segment_start = segment_data['start']
        segment_end = segment_data['end']
        segment_text = segment_data['text']
        segment_tokens = segment_data['tokens']
        segment_temperature = segment_data['temperature']
        segment_avg_logprob = segment_data['avg_logprob']
        segment_compression_ratio = segment_data['compression_ratio']
        segment_no_speech_prob = segment_data['no_speech_prob']'''
    
    text_list = [segment_data['text'] for segment_id, segment_data in segment_dict.items()]
    text_time = [segment_data['start'] for segment_id,segment_data in segment_dict.items()]
    url = segment_dict['url']
    
    chunks_of_ten= chunks(text_list,20)
    sentence_time = text_time[::20]
    
    joined_sentences = [' '.join(chunk) for chunk in chunks_of_ten]
    
    print(len("joined_sentences len: " + joined_sentences))
    print("sentence_time len: " + len(sentence_time))
    

    for index, text in enumerate(joined_sentences):
       
        #Call OpenAI embedding api and input the chunk of text        
        res = openai.Embedding.create(input=text, engine='text-embedding-ada-002')

        #Assign the embedded data to the embeds variable
        embeds = [record['embedding'] for record in res['data']]
        
        # Open a file named "embeds.json" in write mode
        with open("embeds.json", "a") as f:
            # Write the embedded data to the file in JSON format
            json.dump(embeds, f)
        
        
        #prep metadata and upsert batch to Pinecone
        
        vectors = [{
        'id': counter,  # Set the ID key to an incremental value
        'values': res['data'][0]['embedding'],  # Set the values key to the embedded text
        'meta': {
        'url': url,
        'text': text,
        'sentence_time': sentence_time[index]
        }
        }]

        vector_list.append(vectors)
        counter = counter + 1
            
    batch_size = 100

    # Split the vectors into batches of size batch_size
    vector_batches = [vector_list[i:i+batch_size] for i in range(0, len(vector_list), batch_size)]

    print(vector_batches[0])
    #vector_batches_zipped = zip(vector_batches)
    # Upsert each batch to Pinecone
    for vb in vector_batches:
        vb_zipped = zip(vb)
        index.upsert(vectors=list(vb_zipped))

    print("PINECONE UPSERT COMPLETE")

