import os
import streamlit as st #all streamlit commands will be available through the "st" alias
st.set_page_config(page_title="Asistente Personal", layout="wide") #HTML title

import chatbot_lib as glib #reference to local lib script

from vdb_lib import get_collections, show_available_collections, get_retriever, init_collections

from langchain.callbacks import StreamlitCallbackHandler

from sidebar_app import sidebar_params

st.header("⌨️ Chatea con tu asistente personal", help= "Escribe tu pregunta y se invocará el modelo de lenguage seleccionado", divider=True) #page title



if 'memory' not in st.session_state: st.session_state.memory = glib.get_memory() 
if 'chat_history' not in st.session_state: st.session_state.chat_history = [] 



init_collections()


collections = get_collections()
if len(collections):
    col1, col2 = st.columns([3, 1])
    show_available_collections(col2)
else:
    col1  =  st

def show_chat_history(place):
    for message in st.session_state.chat_history: 
        with place.chat_message(message["role"]):
            st.markdown(message["text"]) 


show_chat_history(col1)

model_id, temp, max_tokens = sidebar_params()

input_text = st.chat_input("escribe tu mensaje aquí")


if input_text: 
    with col1.chat_message("user"):
        st.markdown(input_text) 
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
    

    placeholder =  col1.empty()


    chat_message = placeholder.chat_message("assistant") # nuevo contenedor para la respuesta
    st_callback = StreamlitCallbackHandler(chat_message) # Callback Handler rellena el contenedor con la respuesta

    with chat_message: 
        using_collections =  st.session_state.using_collections
        chat_response = ""
        if len(using_collections):  
            for collection in using_collections:
                retriever = get_retriever(collection)

                #placeholder.markdown(f"{collection}")
                
                partial_chat_response = glib.get_chat_rag_response( # definido en chatbot_lib.py
                    prompt=input_text, # texto ingresado por el usuario
                    retriever =  retriever,
                    memory=st.session_state.memory, # memoria actual de la conversación
                    streaming_callback=st_callback, # funcion a invocar cuando se genere la respuesta progresiva
                    model_id= model_id, # id del modelo LLM a invocar
                    invocation_kwargs = { # keyworkd args para sobre escribir en la invocación
                        "max_tokens_to_sample": max_tokens, # cantidad máxima de tokens generados
                        "temperature":temp # temperatura (nivel de libertad o creatividad en la generación)
                    }
                )
                chat_response += f"[{collection}]" + partial_chat_response + "\n\n"
        else:
            chat_response = glib.get_chat_response( # definido en chatbot_lib.py
                prompt=input_text, # texto ingresado por el usuario
                memory=st.session_state.memory, # memoria actual de la conversación
                streaming_callback=st_callback, # funcion a invocar cuando se genere la respuesta progresiva
                model_id= model_id, # id del modelo LLM a invocar
                invocation_kwargs = { # keyworkd args para sobre escribir en la invocación
                    "max_tokens_to_sample": max_tokens, # cantidad máxima de tokens generados
                    "temperature":temp # temperatura (nivel de libertad o creatividad en la generación)
                }
            )
        
    placeholder.empty()
        
    col1.chat_message("assistant").write(chat_response) #display bot's latest response
    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history
    