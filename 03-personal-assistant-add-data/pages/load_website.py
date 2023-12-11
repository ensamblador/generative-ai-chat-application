import os
import streamlit as st
import boto3

from langchain.callbacks import StreamlitCallbackHandler


from vdb_lib import (
    clean_name, load_and_split_website,
    init_collections,
    get_collections
)
import chatbot_lib as glib

st.set_page_config(page_title="Asistente Personal", layout="wide") #HTML title


user_name = "personal"
is_local = True

volume= "/data"


if is_local: upload_path = f"{user_name}/upload"
else: upload_path = f"{volume}/{user_name}/upload"

if not os.path.exists(upload_path):
    os.makedirs(upload_path)


init_collections()

collections = get_collections()

with st.form("new_kb_form"):
    st.header("sitio web")
    website_url = st.text_input("website url") 

    nombre = st.text_input("Nombre de la Colección")
    splitby = st.sidebar.slider("Dividir documento por caracteres", 500, 3000, 1000, 100)
    submitted = st.form_submit_button("Submit")

    if submitted:
        docs = load_and_split_website(website_url, splitby)
        print("len:", len(docs))
        nombre = clean_name(nombre)
        vectordb = st.session_state.chroma_client.create_vectordb(nombre)
        st.session_state.chroma_client.add_docs(nombre, docs, 10)
        print(st.session_state.chroma_client.vectordbs)


st.header("Prueba los documentos indexados")
input_text = st.chat_input("ingresa tu consulta acá")  # display a chat input box

if input_text:  # run the code in this if block after the user submits a chat message
    with st.chat_message("user"):  # display a user chat message
        st.markdown(input_text)  # renders the user's latest message

    placeholder = st.empty()

    chat_message = placeholder.chat_message(
        "assistant"
    )  # nuevo contenedor para la respuesta
    st_callback = StreamlitCallbackHandler(
        chat_message
    )  # Callback Handler rellena el contenedor con la respuesta

    print(st.session_state.chroma_client.vectordbs)

    with chat_message:
        chat_response = glib.test_vector_db(  # definido en chatbot_lib.py
            prompt=input_text,  # texto ingresado por el usuario
            vector_db=st.session_state.chroma_client.get_vectordb(clean_name(nombre)),
            streaming_callback=st_callback,  # funcion a invocar cuando se genere la respuesta progresiva
        )

    placeholder.empty()

    st.chat_message("assistant").write(
        chat_response,
    )  # display bot's latest response
