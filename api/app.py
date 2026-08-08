from fastapi import FastAPI
from api.schemas import ChatRequest

app = FastAPI()

agent = None


def set_agent(graph):
    global agent
    agent = graph


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI and uv!"}


@app.post("/chat")
async def chat(request: ChatRequest):

    if agent is None:
        return {"error": "Agent is not initialized"}

    result = agent.process_query(request.query)

    return {
        "answer": result["final_answer"],
        "total_time": result["total_time"],
        "llm_calls": result["llm_calls"],
        "cache_hit": result["cache_hit"]
    }