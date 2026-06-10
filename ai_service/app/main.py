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

    if "customer" in user_message:
        return {
            "response":"you really want to know about the customer . in next message i send you customer details"
        }
    elif "product" in user_message:
        return {
         "response":"you really want to know about the product details data. in next contact i send you details about those products"
        }
    elif "invoice" in user_message:
        return {
            "response": "You asked for invoice information. Next we will connect this to Odoo invoices."
        }

    elif "sale" in user_message or "sales" in user_message:
        return {
            "response": "You asked for sales information. Next we will connect this to Odoo sales orders."
        }

    else:
        return {
            "response": "I received your message, but I do not understand the ERP command yet."
        }

    return {
        "response": f"FastAPI received your message: {user_message}"
    }
