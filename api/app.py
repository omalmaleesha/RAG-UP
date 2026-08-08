from fastapi import FastAPI
from schemas import ChatRequest

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI and uv!"}


@app.post("/chat")
async def chat(request: ChatRequest):
    query = request.query

    # Later:
    # result = await run_agent(query, request.user_id)

    return {
        "answer": f"Received: {query}"
    }