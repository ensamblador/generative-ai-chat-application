from langchain.memory import ConversationSummaryBufferMemory, ConversationSummaryMemory
from langchain.llms.bedrock import Bedrock
from langchain.chains import ConversationChain
from langchain.chains import RetrievalQA
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate


import streamlit as st
model_kwargs = { 
    "max_tokens_to_sample": 1024, 
    "temperature": 1, 
    "top_p": 0.9, 
    "stop_sequences": ["Human:"]
}

default_model_id = "anthropic.claude-v2:1"

# Clase para llevar la cuenta de los tokens utilizados por el modelo


def get_llm(streaming_callback=None, invocation_kwargs=None, model_id=None):
    
    this_model_id = model_id if model_id else default_model_id # si viene un model_id se usa ese, caso contrario se usa el default
    bedrock_base_kwargs = dict(model_id=default_model_id, model_kwargs= model_kwargs)
    
    if invocation_kwargs: # en el caso de hacer override de invocation_kwargs tales como temperatura y max tokens
        bedrock_base_kwargs = dict(model_id=this_model_id, model_kwargs= {**model_kwargs, **invocation_kwargs})

    new_kwargs = dict(**bedrock_base_kwargs)

    if streaming_callback: # la respuesta tiene que ser en streamin?, pasamos streaming_callback al modelo
        new_kwargs = dict(**bedrock_base_kwargs, streaming=True,callbacks=[streaming_callback])

    print("new_kwargs:",new_kwargs)

    llm = Bedrock(**new_kwargs)
    
    return llm


def get_memory(): 
    
    # ConversationSummaryBufferMemory requiere un LLM para resumir los mensajes viejos
    # Permite mantener la idea sin extender más alla de limite

    llm = get_llm()
    
    memory1 = ConversationSummaryBufferMemory(
        llm=llm, max_token_limit=512,
        memory_key="chat_history",
        return_messages=True,
        human_prefix = "H", ai_prefix= "A" 
    ) 
    memory2 = ConversationSummaryMemory(
        return_messages=True,
        llm=llm, max_token_limit=512, ai_prefix="A", human_prefix="H", memory_key="chat_history")
    
    return memory1


def get_chat_response(prompt, memory, streaming_callback=None,invocation_kwargs=None, model_id= None):
    
    llm = get_llm(streaming_callback, invocation_kwargs, model_id) 
    


    
    base_prompt = """The following is a friendly conversation between a human and an AI. 
    The AI is talkative and provides lots of specific details from its context. 
    If the AI does not know the answer to a question, it truthfully says it does not know.

    Current conversation:
    {chat_history}

    Human:{input}

    Assistant:"""


    BASE_PROMPT_TEMPLATE = PromptTemplate(input_variables=["chat_history", "question"],template=base_prompt)

    conversation_with_summary = ConversationChain( #create a chat client
        llm = llm, #using the Bedrock LLM
        prompt= BASE_PROMPT_TEMPLATE,
        memory = memory, #with the summarization memory
        verbose = True #print out some of the internal states of the chain while running
    )


    inputs_pre = conversation_with_summary.prep_inputs({"input": prompt})
    print (inputs_pre)
    final_input  =  conversation_with_summary.prompt.template.format(chat_history=inputs_pre['chat_history'], input=inputs_pre['input'])

    return conversation_with_summary.predict(input=prompt)


def get_chat_rag_response(prompt, retriever, memory, streaming_callback=None,invocation_kwargs=None, model_id= None):
    
    llm = get_llm(streaming_callback, invocation_kwargs, model_id) 


    qa = ConversationalRetrievalChain.from_llm(
        llm,
        verbose=True,
        retriever=retriever,
        memory=memory,
        get_chat_history=lambda h : h
    ) 


    return qa.run({"question": prompt})



def test_vector_db(prompt, vector_db, streaming_callback=None):
    llm = get_llm(streaming_callback) 
    retriever= vector_db.as_retriever(search_type = "mmr",  search_kwargs={"k": 8})

    qa_chain = RetrievalQA.from_chain_type( llm, verbose=True, retriever=retriever)

    return qa_chain.run({"query": prompt, })
