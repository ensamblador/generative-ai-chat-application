from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain
from anthropic import Anthropic

antro_client = Anthropic()


model_kwargs = { 
    "max_tokens_to_sample": 1024, 
    "temperature": 1, 
    "top_p": 0.9, 
    "stop_sequences": ["Human:"]
}

default_model_id = "anthropic.claude-instant-v1"

# Clase para llevar la cuenta de los tokens utilizados por el modelo
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


def get_llm(streaming_callback=None, invocation_kwargs=None, model_id=None):
    
    this_model_id = model_id if model_id else default_model_id # si viene un model_id se usa ese, caso contrario se usa el default
    bedrock_base_kwargs = dict(model_id=default_model_id, model_kwargs= model_kwargs)
    
    if invocation_kwargs: # en el caso de hacer override de invocation_kwargs tales como temperatura y max tokens
        bedrock_base_kwargs = dict(model_id=this_model_id, model_kwargs= {**model_kwargs, **invocation_kwargs})

    new_kwargs = dict(**bedrock_base_kwargs)

    if streaming_callback: # la respuesta tiene que ser en streamin?, pasamos streaming_callback al modelo
        new_kwargs = dict(**bedrock_base_kwargs, streaming=True,callbacks=[streaming_callback])

    #print("new_kwargs:",new_kwargs)

    llm = Bedrock(**new_kwargs)
    
    return llm


def get_memory(): 
    
    # ConversationSummaryBufferMemory requiere un LLM para resumir los mensajes viejos
    # Permite mantener la idea sin extender más alla de limite

    llm = get_llm()
    
    memory = ConversationSummaryBufferMemory(
        llm=llm, max_token_limit=512,
        human_prefix = "H", ai_prefix= "A" # Prefijos d usuartio y asistente custom para la historia.
    ) 

    return memory


def get_token_counter():
    global token_counter
    token_counter = TokenCounter()
    return token_counter



def get_chat_response(prompt, memory, streaming_callback=None,invocation_kwargs=None, model_id= None, input_token_placeholder=None):
    
    global token_counter

    llm = get_llm(streaming_callback, invocation_kwargs, model_id) 
    
    conversation_with_summary = ConversationChain( #create a chat client
        llm = llm, #using the Bedrock LLM
        memory = memory, #with the summarization memory
        verbose = True #print out some of the internal states of the chain while running
    )
    conversation_with_summary.prompt.template ="""The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context. 
    If the AI does not know the answer to a question, it truthfully says it does not know.

    Current conversation:
    {history}

    Human:{input}

    Assistant:"""

    #final_message  =  conversation_with_summary.prompt.template.format(history=memory., input=prompt)
    #print (final_message)
    inputs_pre = conversation_with_summary.prep_inputs({"input": prompt})
    # print (inputs_pre)
    final_input  =  conversation_with_summary.prompt.template.format(history=inputs_pre['history'], input=inputs_pre['input'])
    #print (final_input)

    all_input_tokens = antro_client.count_tokens(final_input)
    prompt_input_tokens = antro_client.count_tokens(prompt)


    token_counter.new_input(user_input=prompt, all_input=final_input)
    print ("Prompt input tokens:", prompt_input_tokens)
    print ("Prompt input words:", len(prompt.split(" ")))
    print ("All input tokens:", all_input_tokens)
    print ("All input words:", len(final_input.split(" ")))

    if input_token_placeholder:
        input_token_placeholder.markdown(f"""
            | Tokens Entrada | Cantidad|
            |--|:--:|
            |User Mensaje |{token_counter.user_input_tokens}| 
            |Mensaje + Contexto| {token_counter.all_input_tokens}|
            |Acumulado | {token_counter.total_input_tokens}|""")

    return conversation_with_summary.predict(input=prompt)

