
import shutil
import re
import os
import chromadb
from langchain.vectorstores import Chroma
from langchain.document_loaders import S3FileLoader, PyPDFLoader

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import BedrockEmbeddings 
import streamlit as st

bedrock_embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v1")


class CustomChromaClass():
    def __init__(self) -> None:
        self.persistent_client = chromadb.PersistentClient()
        collections = self.persistent_client.list_collections()
        print(collections)
        self.vectordbs = {}
        for collection in collections:
            langchain_chroma = Chroma( client=self.persistent_client,collection_name=collection.name, embedding_function=bedrock_embeddings)
            self.vectordbs[collection.name] = langchain_chroma
        self.vectordb = False
    def create_vectordb(self, name):
        name =  clean_name(name)
        vectordb = Chroma(client=self.persistent_client, embedding_function=bedrock_embeddings,collection_name=name)
        self.vectordbs[name] = vectordb
        self.vectordb = vectordb
        print (self.vectordb._collection.count())
        return vectordb
    
    def get_vectordb(self, name):
        return self.vectordbs[name]

    def add_docs(self, collection_name, docs, n=10):
        add_docs_by_chunks(self.vectordbs[collection_name], docs, n)



def init_collections():
    if 'chroma_client' not in st.session_state: st.session_state.chroma_client =  CustomChromaClass()
    if 'using_collections' not in st.session_state: st.session_state.using_collections = []



def save_file_local(bytes, filename, path):
    with open (f"{path}/{filename}", "wb") as f:
        f.write(bytes)
    return True

def load_and_split_pdf(file_path, splitby):

    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\. ", " ", ""],
        chunk_size=splitby,
        chunk_overlap=int(splitby/10),
        length_function=len
    )

    loader = PyPDFLoader(file_path)
    docs = loader.load_and_split(text_splitter)
    return docs



def produce_docs(s3_bucket, s3_keys, splitby):
    all_docs = []


    text_splitter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", "\. ", " ", ""],
        chunk_size=splitby,
        chunk_overlap=int(splitby/10),
        length_function=len
    )

    for s3_key in s3_keys:
        print (f"loading: {s3_key}", end="")
        loader = S3FileLoader(s3_bucket, s3_key)
        pages = loader.load()
        print(len(pages[0].page_content), "chars ", end="")
        docs = text_splitter.split_documents(pages)
        print (len(docs), "chunks")

        all_docs += docs
    return all_docs

def clean_name(name):
    return re.sub(r'[^a-z0-9_]', '_', name.lower()) 

def create_vectordb(persistent_client, name):
    vectordb = Chroma(client=persistent_client, embedding_function=bedrock_embeddings,collection_name=name)
    print(vectordb._collection.count())
    return vectordb



def add_docs_by_chunks(vector_database, docs, n =10):
    n_docs =  len (docs)
    n_docs_ingested = 0
    porcentaje_ingested = int(n_docs_ingested/n_docs)
    chunks = [docs[i:i+n] for i in range(0,n_docs, n)]

    print("Largo total, chunks, largo chunk, largo ultimo chunk", n_docs, len(chunks), len(chunks[0]), len(chunks[-1]))
    progress_bar = st.progress(0, text=f"vectorizando documentos: {porcentaje_ingested}%")

    for chunk in chunks:
        vector_database.add_documents( documents=chunk)
        n_docs_ingested += len(chunk)
       
        porcentaje_ingested = int(n_docs_ingested*100/n_docs)
        print("Ingestando:", porcentaje_ingested)
        progress_bar.progress(porcentaje_ingested, f"vectorizando documentos: {n_docs_ingested}")

    print("Documentos Ingestados:", vector_database._collection.count())
    progress_bar.progress(porcentaje_ingested, f"documentos vectorizados: {n_docs_ingested} OK")






def get_collections():
    if 'chroma_client' in st.session_state: 
        collections  = st.session_state.chroma_client.persistent_client.list_collections()
        return collections
    return []
    

def get_retriever(name):
     if 'chroma_client' in st.session_state: 
        print(st.session_state.chroma_client.vectordbs)
        vector_db = st.session_state.chroma_client.vectordbs[name]
        return vector_db.as_retriever(search_type = "mmr",  search_kwargs={"k": 5})



def collection_click(name):
    using_collections =  st.session_state.using_collections
    is_used = name in using_collections
    if is_used: using_collections.remove(name)
    else: using_collections.append(name)

    print(using_collections)



def show_available_collections(place):
    place.write("**Bases de conocimiento disponibles**")
    collections = get_collections()
    using_collections =  st.session_state.using_collections
    for collec in collections:
        checked = collec.name in using_collections
        place.checkbox(collec.name,value=checked, on_change=collection_click, kwargs = dict(name=collec.name) )