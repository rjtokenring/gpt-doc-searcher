from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import OpenSearchVectorSearch
from langchain import OpenAI
from langchain.chains import RetrievalQA
import os

class EsClient:
    
    def __init__(self):
        embeddings = OpenAIEmbeddings()
        
        es_url = os.getenv('ES_URL')
        if es_url is None:
            es_url = "http://localhost:9200"
        
        docsearch = OpenSearchVectorSearch(index_name="vstore-indexed", 
                                            embedding_function=embeddings,
                                            opensearch_url=es_url)
        
        qa = RetrievalQA.from_chain_type(llm=OpenAI(),
                                chain_type="stuff",
                                retriever=docsearch.as_retriever())
        
        self.queryclient = qa
    
    def query(self, q):
        return self.queryclient.run(q)