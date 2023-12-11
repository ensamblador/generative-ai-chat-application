import streamlit as st


def sidebar_params():
    st.sidebar.header('Parametros 🎛️')

    options = ['anthropic.claude-instant-v1','anthropic.claude-v1', 'anthropic.claude-v2',  'anthropic.claude-v2:1'] 
    model_id = st.sidebar.selectbox('model_id', options,3)

    temp = st.sidebar.slider('Temperatura 🌡️', 0.0, 1.0, 0.0, 0.01)
    max_tokens = st.sidebar.slider('Max Tokens 🫷', 50, 10000, 1500, 50)

    return model_id, temp, max_tokens
