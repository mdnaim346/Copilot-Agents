from odoo import api,models,fields

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

            if response.status_code == 200:
                data = response.json()
                record.ai_response = data.get("response")
            else:
                record.ai_response = "FastAPI error"
    
