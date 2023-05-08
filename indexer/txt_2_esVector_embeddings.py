from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import OpenSearchVectorSearch
from langchain import OpenAI
from langchain.chains import RetrievalQA
import getopt, sys

argumentList = sys.argv[1:]
 
# Options
options = "hd:e:"
 
# Long options
long_options = ["dir", "es_url", "help"]

es_url = "http://localhost:9200"
directory = "../data/"

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--help"):
            print ("data loader -d <dir> -e <es_url>")
             
        elif currentArgument in ("-d", "--dir"):
            directory = currentValue
             
        elif currentArgument in ("-e", "--es_url"):
            es_url = currentValue
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

print("Loading data from {d}".format(d=directory))
print("Connecting to ES cluster {e}".format(e=es_url))

embeddings = OpenAIEmbeddings()

loader = DirectoryLoader(directory, glob="**/*.txt")
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=2500, chunk_overlap=0)

texts = text_splitter.split_documents(documents)

docsearch = OpenSearchVectorSearch(index_name="vstore-indexed", 
    embedding_function=embeddings,
    opensearch_url=es_url)

print("Starting indexing...")
print("Discovered {l} documents".format(l=len(documents)))

docsearch.add_documents(texts)

print("Done...")
