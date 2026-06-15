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
            intent = data.get("intent")

            if intent == "customer_list":
                record.ai_response = record._get_customer_list()

            elif intent == "product_list":
                record.ai_response = record._get_product_list()

            elif intent == "customer_count":
                record.ai_response = record._get_customer_count()

            elif intent == "product_count":
                record.ai_response = record._get_product_count()

            elif intent == "sale_count":
                record.ai_response = record._get_sales_count()

            elif intent == "quotation_count":
                record.ai_response = record._get_quotation_count()

            elif intent == "invoice_count":
                record.ai_response = record._get_invoice_count()

            elif intent == "invoice_list":
                record.ai_response = record._get_invoice_list()

            else:
                record.ai_response = data.get("message") or data.get("response", "Unknown command.")

           

            # response = requests.post(url, json=payload, timeout=20)

            # if response.status_code == 200:
            #     data = response.json()
            #     record.ai_response = data.get("response")
            # else:
            #     record.ai_response = "FastAPI error"

    def _has_model(self, model_name):
        return model_name in self.env.registry.models

    def _missing_app_message(self, feature_name, app_name):
        return f"{feature_name} is not available. Please install the {app_name} app first."

    def _get_customer_domain(self):
        partner_model = self.env["res.partner"]
        if "customer_rank" in partner_model._fields:
            return [("customer_rank", ">", 0)]
        return []

    def _get_customer_list(self):
        customers = self.env["res.partner"].search(
            self._get_customer_domain(),
            limit=10
        )

        if not customers:
            return "No customers found."

        return "Customers: " + ", ".join(customers.mapped("name"))


    def _get_customer_count(self):
        count = self.env["res.partner"].search_count(self._get_customer_domain())

        return f"Total customers: {count}"

    def _get_product_list(self):
        if not self._has_model("product.product"):
            return self._missing_app_message("Products", "Inventory/Product")

        products = self.env["product.product"].search([], limit=10)

        if not products:
            return "No products found."

        return "Products: " + ", ".join(products.mapped("display_name"))


    def _get_product_count(self):
        if not self._has_model("product.product"):
            return self._missing_app_message("Product count", "Inventory/Product")

        count = self.env["product.product"].search_count([])

        return f"Total products: {count}"


    def _get_sales_count(self):
        if not self._has_model("sale.order"):
            return self._missing_app_message("Sales count", "Sales")

        count = self.env["sale.order"].search_count([
            ("state", "in", ["sale", "done"])
        ])

        return f"Total confirmed sales orders: {count}"


    def _get_quotation_count(self):
        if not self._has_model("sale.order"):
            return self._missing_app_message("Quotation count", "Sales")

        count = self.env["sale.order"].search_count([
            ("state", "in", ["draft", "sent"])
        ])

        return f"Total quotations: {count}"

    def _get_invoice_count(self):
        if not self._has_model("account.move"):
            return self._missing_app_message("Invoice count", "Invoicing/Accounting")

        count = self.env["account.move"].search_count([
            ("move_type", "in", ["out_invoice", "out_refund"])
        ])

        return f"Total customer invoices: {count}"

    def _get_invoice_list(self):
        if not self._has_model("account.move"):
            return self._missing_app_message("Invoices", "Invoicing/Accounting")

        invoices = self.env["account.move"].search([
            ("move_type", "in", ["out_invoice", "out_refund"])
        ], limit=10)

        if not invoices:
            return "No invoices found."

        return "Invoices: " + ", ".join(invoices.mapped("name"))
    
