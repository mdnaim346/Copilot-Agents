from fastapi import FastAPI
from pydantic import BaseModel




app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def  home():
    return {"status": "Ok"}

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message

    return {
        "response": f"FastAPI received your message: {user_message}"
    }
