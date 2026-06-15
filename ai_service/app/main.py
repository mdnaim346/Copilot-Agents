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
    user_message = request.message.lower()

    if (
        "customer_count" in user_message
        or "customer count" in user_message
        or ("count" in user_message and "customer" in user_message)
    ):
        return{
            "intent": "customer_count",
            "message": "user wants customer count"
        }
    elif any(keyword in user_message for keyword in ("customer", "customers", "customer_details")):
        return {
            "intent": "customer_list",
            "message":"customer data want to  see"
        }

    elif (
        "product_count" in user_message
        or "product count" in user_message
        or ("count" in user_message and "product" in user_message)
    ):
        return{
            "intent": "product_count",
            "message": "user wants product count"
        }
    elif any(keyword in user_message for keyword in ("product", "products", "product_details")):
        return {
            "intent": "product_list",
            "message":"prodict data want to  see"
        }
    elif (
        "invoice_count" in user_message
        or "invoice count" in user_message
        or ("count" in user_message and "invoice" in user_message)
    ):
        return{
            "intent": "invoice_count",
            "message": "user wants invoice count"
        }
    elif "invoice" in user_message:
        return {
            "intent": "invoice_list",
            "message": "user wants invoice list"
        }

    elif (
        "sale_count" in user_message
        or "sale count" in user_message
        or "sales count" in user_message
        or ("count" in user_message and ("sale" in user_message or "sales" in user_message))
    ):
        return{
            "intent": "sale_count",
            "message": "user wants sale count"
        }
    elif (
        "quotation_count" in user_message
        or "quotation count" in user_message
        or ("count" in user_message and "quotation" in user_message)
    ):
        return{
            "intent": "quotation_count",
            "message": "user wants quotation count"
        }
    elif "sale" in user_message or "sales" in user_message:
        return {
            "response": "You asked for sales information. Next we will connect this to Odoo sales orders."
        }

    else:
        return {
            "response": "I received your message, but I do not understand the ERP command yet."
        }
    

  
