from odoo import models, fields

import requests

class AIChat(models.Model):
    _name= "ai.copilot.chat"
    _description= "AI Copilot Chat Messages"

    user_message= fields.Char(string="User message")
    ai_response=fields.Char(string="AI response")

    def action_send_message(self):
        for record in self:
            url = "http://127.0.0.1:8000/chat"
            payload = {
                "message": record.user_message or ""
            }
            response = requests.post(url, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()

            if data.get("intent") == "customer_list":
                Partner = self.env["res.partner"].sudo()
                domain = [("customer_rank", ">", 0)] if "customer_rank" in Partner._fields else []
                customers = Partner.search(domain, limit=10)
                customer_names="\n".join(customers.mapped("name"))
                record.ai_response= f"some related customers are :\n{customer_names}"
            else:
                record.ai_response=data.get("message") or data.get("response") or "I received your message."

           

            # response = requests.post(url, json=payload, timeout=20)

            # if response.status_code == 200:
            #     data = response.json()
            #     record.ai_response = data.get("response")
            # else:
            #     record.ai_response = "FastAPI error"
    
