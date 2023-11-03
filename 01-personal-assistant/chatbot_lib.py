from langchain.memory import ConversationSummaryBufferMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain


model_kwargs = { 
    "max_tokens_to_sample": 1024, 
    "temperature": 1, 
    "top_p": 0.9, 
    "stop_sequences": ["Human:"]
}

default_model_id = "anthropic.claude-instant-v1"


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
        llm=llm, max_token_limit=1024,
        human_prefix = "H", ai_prefix= "A" # Prefijos d usuartio y asistente custom para la historia.
    ) 
    return memory



def get_chat_response(prompt, memory, streaming_callback=None,invocation_kwargs=None, model_id= None):
    
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
    return conversation_with_summary.predict(input=prompt)

