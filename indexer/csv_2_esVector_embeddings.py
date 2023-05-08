from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.vectorstores import OpenSearchVectorSearch
from langchain import OpenAI
from langchain.chains import RetrievalQA
import getopt, sys

argumentList = sys.argv[1:]
 
# Options
options = "hf:e:"
 
# Long options
long_options = ["file", "es_url", "help"]

es_url = "http://localhost:9200"
csvfile = "../data-csv/input.csv"

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--help"):
            print ("data loader -d <dir> -e <es_url>")
             
        elif currentArgument in ("-f", "--file"):
            csvfile = currentValue
             
        elif currentArgument in ("-e", "--es_url"):
            es_url = currentValue
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))

print("Loading data from file {d}".format(d=csvfile))
print("Connecting to ES cluster {e}".format(e=es_url))

embeddings = OpenAIEmbeddings()

loader = CSVLoader(file_path=csvfile, csv_args={
    'delimiter': ',',
    'quotechar': '"'
})
documents = loader.load()

docsearch = OpenSearchVectorSearch(index_name="vstore-indexed", 
    embedding_function=embeddings,
    opensearch_url=es_url)

print("Starting indexing...")
print("Discovered {l} documents".format(l=len(documents)))

docsearch.add_documents(documents)

print("Done...")
