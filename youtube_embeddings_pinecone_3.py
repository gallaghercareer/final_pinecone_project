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

def embed_vectors():
   
    #openai_key
    #openai.api_key = read_api_key('config.txt')
    openai.api_key = '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'
   
    #pinecone_key
    #pinecone_key = read_api_key('pinecone_config.txt') 
    pinecone_key = 'a4859682-4450-4789-8cb0-5b856ccc29a0'

    #Connect to Pinecone API
    pinecone.init(api_key=pinecone_key,environment = 'us-east1-gcp')

    #check if index database already exists (only create index if it doesn't)
    if 'index-test' not in pinecone.list_indexes():
        # print('vector database created')
        pinecone.create_index('index-test',dimension=len(embeds[0]))
        #else:
        #print("vector database already exists")

    #assign pinecone Index object
    index = pinecone.Index('index-test')
    hasVectors = None

    #check Index object stats (vector count)
    indexStats = index.describe_index_stats()
    #print(indexStats)


    #assign vector count to variable
    num_vectors = indexStats.total_vector_count
    #print(num_vectors)
    if num_vectors > 0 :   
        # print(f"The 'my-index' index contains {num_vectors} vectors.")
        hasVectors = True   
    else:
        # print(f"The index does not contain any vectors")
        hasVectors = False


    cwd = os.getcwd()
    counter = 0
    
    with os.scandir(cwd) as entries:
        transcripts = (entry for entry in entries if entry.is_file() and entry.name.endswith('.txt'))
        
        for transcript in transcripts:
   
    
            #declare ID for all transcript snippets in Vector Database
            vector_batch_id = 0

            #declare vector total for increment
            vectorTotal = 0

            #vector list for every embedding
            vector_list = []


            joined_sentences = []
  
            with open(transcript, 'r') as file:
                segment_dict_str = file.read()
            
            segment_dict = eval(segment_dict_str) 
             
    
            text_list = [segment_data['text'] for segment_id, segment_data in segment_dict.items()]
            text_time = [segment_data['start'] for segment_id,segment_data in segment_dict.items()]
            url = list(segment_dict.values())[0]['url']

    
            chunks_of_ten= chunks(text_list,20)
            sentence_time = text_time[::20]

            joined_sentences = [' '.join(chunk) for chunk in chunks_of_ten]
    

            for idx, text in enumerate(joined_sentences):
       
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
                    'sentence_time': sentence_time[idx]
                }
                }]

                vector_list.extend(vectors)
                counter = counter + 1
            
            batch_size = 100
            
            # Split the vectors into batches of size batch_size
            vector_batches = [vector_list[i:i+batch_size] for i in range(0, len(vector_list), batch_size)]
            #print(vector_batches[0])
            #vector_batches_zipped = zip(vector_batches)
            # Upsert each batch to Pinecone
            for vb in vector_batches:
                vb_tuples = [(str(vector_dict['id']), vector_dict['values'], vector_dict['meta']) for vector_dict in vb]
                index.upsert(vectors=vb_tuples)

        print("PINECONE UPSERT COMPLETE")

  