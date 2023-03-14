import download_mp3_1 
#import embeddings_pinecone_3
import whisper_transcribe_2

#Define a function to read in a single line file
def read_api_key(input_file):
    # Open the file in read mode
    with open(input_file, 'r') as file:
        # Read the contents of the file as a string
        string_variable = file.read()
        return string_variable
'''
#configuration settings:
 	#openai_key
    openai.api_key = read_api_key('config.txt')
    #pinecone_key
    pinecone_key = read_api_key('pinecone_config.txt')    

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
'''

#input("Enter the channelID to download MP3s. Enter a second arg for limit (leave blank if you want to download entire youtube channel): ")
#download_mp3_1.download_mp3s('UCv83tO5cePwHMt1952IVVHw',1)

#download_mp3_1.download_mp3s('UCv83tO5cePwHMt1952IVVHw')
whisper_transcribe_2.transcribe_mp3()







