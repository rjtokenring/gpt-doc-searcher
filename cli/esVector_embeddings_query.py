from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import DirectoryLoader
from langchain.vectorstores import OpenSearchVectorSearch
from langchain import OpenAI
from langchain.chains import RetrievalQA
import getopt, sys

argumentList = sys.argv[1:]
 
# Options
options = "he:"
 
# Long options
long_options = ["es_url", "help"]

es_url = "http://localhost:9200"

try:
    # Parsing argument
    arguments, values = getopt.getopt(argumentList, options, long_options)
     
    # checking each argument
    for currentArgument, currentValue in arguments:
 
        if currentArgument in ("-h", "--help"):
            print ("query cli -e <es_url>")
             
        elif currentArgument in ("-e", "--es_url"):
            es_url = currentValue
             
except getopt.error as err:
    # output error, and return with an error code
    print (str(err))


print("Starting query cli...")
print("Connecting to ES cluster {e}".format(e=es_url))

embeddings = OpenAIEmbeddings()

docsearch = OpenSearchVectorSearch(index_name="vstore-indexed", 
    embedding_function=embeddings,
    opensearch_url=es_url)

# Query the vector store
qa = RetrievalQA.from_chain_type(llm=OpenAI(),
                                chain_type="stuff",
                                retriever=docsearch.as_retriever())

def query(q):
    print(f"Query: {q}")
    print(f"Answer: {qa.run(q)}")
    print("------------------------------")


while True:
 input_variable=input()
 if(input_variable=='quit' or input_variable=='exit'):
  break
 else:
  query(input_variable)
  
print("Exiting")  
