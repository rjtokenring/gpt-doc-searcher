# GPT Doc Searcher

GPT based document search. Query YOUR data using LLM.

LLMs are a phenomenonal technologies for knowledge reasoning. They are pre-trained on large amounts of publicly available data.

How can we introduce our own private data into LLMs?

One paradigm is in-context learning (the other is finetuning), where we insert context into the input.
In this way, we can leverage LLM’s reasoning capabilities over private data.

This project uses *LangChain* to extract text from local documents and index them.
Text *embeddings* are generated using [OpenAI Emebddings](https://platform.openai.com/docs/guides/embeddings) and stored in a ES cluster for later vector searches over them.
Then a similarity_search is performed by default using an Approximate k-NN Search over vector stored.

```mermaid
graph LR;
    Client-->Text;
    Text-->ENCODER;
    ENCODER-->Vectors;
	Vectors-->Search;
```

# Pre-reqs

Code is using LangChain and python 3. To install required libraries, use:

```console
pip install langchain openai opensearch-py
```

Examples are based on OpenAI.

To run all examples, you need a valid `OPENAI_API_KEY`. You can register to openai and get a one with some credits. Then set it as environment variable.
`export OPENAI_API_KEY=<key>`

## Indexer

Folder [indexer](indexer) contains samples application that:
- read all files (txt,csv) from a folder
- tokenize text
- create embeddings
- store them in Elasticserach

This is just a simple not scalable example to show the indexing flow. *LangChain* provides differt type of Loaders that can be used to extract content from different sources (like csv, etc.)
ES has been choosen for simplicity of running it in clustered way. Other Vector stores are available and can ve choosen on purpose.

To run indexer, use following syntax:

```console
python3 txt_2_esVector_embeddings.py -e "http://localhost:9200" -d "../data/"
```

A new index called **vstore-indexed** will be created inside cluster and all new discovered document embeddings will be appended into it.

For test, ES can be executed locally

```console
docker pull opensearchproject/opensearch:latest
docker run -d -p 9200:9200 -p 9600:9600 -e "discovery.type=single-node" -e "plugins.security.disabled=true" opensearchproject/opensearch:latest
```

## CLI

Simple REPL utility to query over indexed data and peform vector searches. It can be used to query data just added to ES store.

```console
python3 esVector_embeddings_query.py -e "http://localhost:9200"
```

Type `exit` to terminate.

## DocSearch Microservice

Simple pure python microservice to perform queries on ES vector store using GPT.
Project is composed by a Docker file to build image

```console
cd docsearch-microservice
docker build -t searchopenapims:0.1 .
```

### Run DocSearch Microservice locally (just for test)

```console
docker run -d -p 9000:9000 -e "OPENAI_API_KEY=<key>" -e "ES_URL=http://localhost:9200" searchopenapims:0.1`
```

### API

Microservice can be queries via REST calls.
Here is a search example:

```json
POST http://127.0.0.1:9000/v1/search
Content-Type: application/json

{
  "question": "What is Zerbellifero?"
}
```

answer

```json
{
  "question": "What is Zerbellifero?",
  "answer": " Zerbellifero is a fantasy great animal with large eyes that lives in the wild in America."
}
```
