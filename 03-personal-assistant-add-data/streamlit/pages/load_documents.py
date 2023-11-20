import os
import streamlit as st
import boto3


import chromadb
from langchain.callbacks import StreamlitCallbackHandler

from vdb_lib import save_file_local, load_and_split_pdf, create_vectordb, add_docs_by_chunks, clean_name, init_collections
import chatbot_lib as glib

upload_path= "./upload"

s3client = boto3.client('s3')

s3_bucket = os.environ.get("S3_BUCKET")
s3_path = os.environ.get("S3_PATH")

s3_bucket = "ac-genai-streamlitbucket2fe9c216-4t8poszaf1to"
s3_path = "upload_files"

init_collections()

with st.form("new_kb_form"):
    st.header("Nueva Base de Conocimientos")
    uploaded_files = st.file_uploader("Elija documentos (pdf)", accept_multiple_files=True)
    nombre =  st.text_input("Nombre de la Colección")
    splitby = st.sidebar.slider('Dividir documento por caracteres',500, 3000, 1000, 100)
    submitted = st.form_submit_button("Submit")

    if submitted:
        docs = [] 
        n_files = len(uploaded_files)
        n_processed_files = 0
        porcentaje_progreso  = int(n_processed_files*100/n_files)


        for uploaded_file in uploaded_files:
            
            filename = uploaded_file.name
            full_path_filename = f"{upload_path}/{filename}"
            n_processed_files +=1
            porcentaje_progreso  = int(n_processed_files*100/n_files)

            loading_bar = st.progress(porcentaje_progreso,  text=filename)

            save_file_local(uploaded_file.read(),filename, upload_path )
            docs  += load_and_split_pdf(full_path_filename, splitby)
            loading_bar.empty()
            st.write("✅ " + filename)
            #loading_bar.progress(porcentaje_progreso, text="Archivo: "+ filename)

            #st.stop()

            #destination_key = f"{s3_path}/{uploaded_file.name}"
            #s3_progress_bar = st.progress(0, text=s3_progress_text)
            #s3_progress_text = "Almacenando en la nube"
            #res = s3client.upload_fileobj(uploaded_file,s3_bucket, destination_key)
            
            

            #loader = S3FileLoader(s3_bucket, destination_key)
  

            #if uploaded_file.type == "application/pdf":
                
            #    loader = PyPDFLoader(uploaded_file)
            #    print (uploaded_file.name,"is",uploaded_file.type)


            #with conn.open(f"{s3_bucket}/{s3_path}/{uploaded_file.name}", "wb") as s3_file:
            #    print (uploaded_file.name,":",res)
            #    res = s3_file.write(bytes_data)
        


        print ("len:", len(docs))
        nombre = clean_name(nombre)
        vectordb =   st.session_state.chroma_client.create_vectordb(nombre)
        st.session_state.chroma_client.add_docs(nombre, docs, 10)
        print( st.session_state.chroma_client.vectordbs)


st.header("Prueba los documentos indexados")
input_text = st.chat_input("ingresa tu consulta acá") #display a chat input box

if input_text: #run the code in this if block after the user submits a chat message
    with st.chat_message("user"): #display a user chat message
        st.markdown(input_text) #renders the user's latest message
    
    
    placeholder =  st.empty()


    chat_message = placeholder.chat_message("assistant") # nuevo contenedor para la respuesta
    st_callback = StreamlitCallbackHandler(chat_message) # Callback Handler rellena el contenedor con la respuesta


    print(st.session_state.chroma_client.vectordbs)

    with chat_message: 
        chat_response = glib.test_vector_db( # definido en chatbot_lib.py
            prompt=input_text, # texto ingresado por el usuario
            vector_db = st.session_state.chroma_client.get_vectordb(clean_name(nombre)),
            streaming_callback=st_callback, # funcion a invocar cuando se genere la respuesta progresiva
        )

        
    placeholder.empty()
        
    st.chat_message("assistant").write(chat_response,) #display bot's latest response
