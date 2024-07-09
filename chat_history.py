import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
app = FastAPI()
 
class QueryRequest(BaseModel):
    query: str
    session_id: str

load_dotenv('.env')
# Initializes your app with your bot token and socket mode handler
cohere_api_key=os.environ.get("cohere_api_key")

store = {}

def get_session_history(session_id) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]

def search_query(query, session_id):
    # llm = ChatCohere(cohere_api_key=cohere_api_key, temperature=0)

    # ### Answer question ###
    # qa_system_prompt = """You are an assistant for question-answering tasks. \
    # Use the following pieces of retrieved context to answer the question. \
    # If you don't know the answer, just say that you don't know. \
    # Use three sentences maximum and keep the answer concise.\
        
    # {context}"""
    
    # qa_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         ("system", qa_system_prompt),
    #         MessagesPlaceholder("chat_history"),
    #         ("human", "{input}"),
    #     ]
    # )
    # question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    # session_history = get_session_history(session_id)
    # print(session_history)

    # conversational_rag_chain = RunnableWithMessageHistory(
    # runnable=question_answer_chain,
    # get_session_history=get_session_history,
    # input_messages_key="input",
    # history_messages_key="chat_history",
    # output_messages_key="answer",
    # )

    # context = "This is the context for answering the question."
    # # result = conversational_rag_chain.invoke(
    # # {"input": query})["answer"]

    template = """Name of Assistant is Jarvis and it is a large language model trained by Cohere.

    Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

    Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

    Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

    Previous conversation history:
    {history}

    Human: {human_input}
    Assistant:"""

    prompt = PromptTemplate(
        input_variables=["history", "human_input"], 
        template=template
    )

    llm = ChatCohere(cohere_api_key=cohere_api_key, model='command-r-plus', temperature=0)

    # Ensure the prompt is passed to the ConversationChain
    memory = ConversationBufferMemory()
    conversation_buf = ConversationChain(
        llm=llm,
        prompt=prompt,
        memory=memory,
        input_key="human_input",
        output_key="result"
    )

    result = conversation_buf.invoke(
                {"human_input": query},
                config={"configurable": {"session_id": session_id}}
                )
    
    print(result["result"])
    return result["result"]

@app.post("/search")
async def search(query: QueryRequest):
    try:
        result = search_query(query.query, query.session_id)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




