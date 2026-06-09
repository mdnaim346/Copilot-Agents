from odoo import api,models,fields

class AIChat(models.Model):
    _name= "ai.chat"
    _description= " Ai chat messeges"

    user_messege= fields.Char(string = "User messege")
    ai_response=fields.Char(string="AI response")
    