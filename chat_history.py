import os
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_cohere import ChatCohere
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
 
app = FastAPI()
 
class QueryRequest(BaseModel):
    query: str
    # session_id: str

load_dotenv('.env')
# Initializes your app with your bot token and socket mode handler
cohere_api_key=os.environ.get("cohere_api_key")

# store = {}

# def get_session_history(session_id) -> BaseChatMessageHistory:
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]

def search_query(query):
    llm = ChatCohere(cohere_api_key=cohere_api_key, temperature=0)

    ### Answer question ###
    qa_system_prompt = """You are an assistant for question-answering tasks. \
    Use the following pieces of retrieved context to answer the question. \
    If you don't know the answer, just say that you don't know. \
    Use three sentences maximum and keep the answer concise.\

    {context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    conversational_rag_chain = RunnableWithMessageHistory(
    question_answer_chain,
    input_messages_key="input",
    history_messages_key="chat_history",
    output_messages_key="answer",
    )

    result = conversational_rag_chain.invoke(
    {"input": query})["answer"]

    return result

@app.post("/search")
async def search(query: QueryRequest):
    try:
        result = search_query(query.query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)




