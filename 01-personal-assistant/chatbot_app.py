import streamlit as st #all streamlit commands will be available through the "st" alias
import chatbot_lib as glib #reference to local lib script
from langchain.callbacks import StreamlitCallbackHandler



st.set_page_config(page_title="Asistente Personal") #HTML title
st.markdown("## Chatea con tu asistente personal") #page title



if 'memory' not in st.session_state: #see if the memory hasn't been created yet
    st.session_state.memory = glib.get_memory() #initialize the memory


if 'chat_history' not in st.session_state: #see if the chat history hasn't been created yet
    st.session_state.chat_history = [] #initialize the chat history


#Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
for message in st.session_state.chat_history: #loop through the chat history
    with st.chat_message(message["role"]): #renders a chat line for the given role, containing everything in the with block
        st.markdown(message["text"]) #display the chat content


st.sidebar.markdown('## Parametros')

options = ['anthropic.claude-instant-v1', 'anthropic.claude-v2'] 
model_id = st.sidebar.selectbox('model_id', options)

temp = st.sidebar.slider('Temperatura', 0.0, 1.0, 0.0, 0.01)
max_tokens = st.sidebar.slider('Max Tokens', 50, 10000, 1024, 50)


input_text = st.chat_input("escribe tu mensaje aquí") #display a chat input box

if input_text: #run the code in this if block after the user submits a chat message
    with st.chat_message("user"): #display a user chat message
        st.markdown(input_text) #renders the user's latest message
    
    st.session_state.chat_history.append({"role":"user", "text":input_text}) #append the user's latest message to the chat history
    

    placeholder =  st.empty()


    chat_message = placeholder.chat_message("assistant") # nuevo contenedor para la respuesta
    st_callback = StreamlitCallbackHandler(chat_message) # Callback Handler rellena el contenedor con la respuesta



    with chat_message: 
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
        
    st.chat_message("assistant").write(chat_response,) #display bot's latest response


    st.session_state.chat_history.append({"role":"assistant", "text":chat_response}) #append the bot's latest message to the chat history
    