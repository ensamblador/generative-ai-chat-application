import streamlit as st
from anthropic import Anthropic

antro_client = Anthropic()

class TokenCounter():
    def __init__(self) -> None:
        self.user_input_tokens = 0
        self.all_input_tokens = 0
        self.output_tokens = 0
        self.total_input_tokens = 0
        self.total_output_tokens = 0
    def new_input(self, user_input, all_input):
        all_input_tokens = antro_client.count_tokens(all_input)
        user_input_tokens = antro_client.count_tokens(user_input)
        self.user_input_tokens = user_input_tokens
        self.all_input_tokens = all_input_tokens
        self.total_input_tokens +=all_input_tokens
        print (self.all_input_tokens)


    def new_output(self, output):
        output_tokens = antro_client.count_tokens(output)
        self.output_tokens = output_tokens

        self.total_output_tokens +=output_tokens

def init_token_counter():
    if 'token_counter' not in st.session_state: st.session_state.token_counter = TokenCounter()
