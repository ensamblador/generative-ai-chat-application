import streamlit as st


def sidebar_params():
    st.sidebar.header('Parametros 🎛️')

    options = ['anthropic.claude-instant-v1', 'anthropic.claude-v2'] 
    model_id = st.sidebar.selectbox('model_id', options)

    temp = st.sidebar.slider('Temperatura 🌡️', 0.0, 1.0, 0.0, 0.01)
    max_tokens = st.sidebar.slider('Max Tokens 🫷', 50, 10000, 1024, 50)

    return model_id, temp, max_tokens



def token_placeholder():

    st.sidebar.markdown('### Contador Tokens')
    token_placeholder = st.sidebar.empty()

    token_placeholder.markdown(f"""
        | Tokens Entrada | Cantidad|
        | --|:--:|
        | User Mensaje |0| 
        |Mensaje + Contexto| 0|
        |Acumulado | 0""")

    st.sidebar.markdown("  ")

    output_placeholder = st.sidebar.empty()

    output_placeholder.markdown(f"""
        | Tokens Respuesta   | Cantidad|
        | --|:--:|
        |Ultima respuesta| 0|
        |Acumulado | 0""")
    

    return token_placeholder, output_placeholder


def update_output_tokens(text, output_placeholder):
    st.session_state.token_counter.new_output(text)
    output_placeholder.markdown(f"""
            | Tokens Respuesta   | Cantidad|
            | --|:--:|
            |Ultima respuesta| { st.session_state.token_counter.output_tokens}|
            |Acumulado | { st.session_state.token_counter.total_output_tokens} |""")
    


def update_input_tokens(user_input, all_input, total_input, input_token_placeholder):
    if input_token_placeholder:
        input_token_placeholder.markdown(f"""
            | Tokens Entrada | Cantidad|
            |--|:--:|
            |User Mensaje |{ user_input}| 
            |Mensaje + Contexto| { all_input}|
            |Acumulado | { total_input}|""")