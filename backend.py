from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from config import *
from langchain_cohere import ChatCohere
from langchain.agents import AgentType, initialize_agent, load_tools
 
app = FastAPI()
 
class QueryRequest(BaseModel):
    query: str
 
# Set environment variables for API keys
os.environ['cohere_api_key'] = "<cohere_api_key>"
os.environ['OPENWEATHERMAP_API_KEY'] = "<OPENWEATHERMAP_API_KEY>"
os.environ['serpapi_api_key'] = "<serpapi_api_key>"
 
 
def search_query(query: str):
    custom_prompt = (
        "You are a knowledgeable assistant. When asked about any topic, provide a detailed and comprehensive response. "
        "Include background information, key points, significant achievements, relevant current events, and any controversies. "
        "Ensure your answer is well-rounded and informative."
    )
 
    llm = ChatCohere(cohere_api_key=cohere_api, model='command-r-plus', temperature=0)
    tools = load_tools(["serpapi" , 'openweathermap-api'], llm)
 
    agent_chain = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        prompt=custom_prompt
    )
    result = agent_chain.run(query)
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