from odoo import models, Command


class EstateAccount(models.Model):
    _inherit = "estate.property"

    def sold(self):
        journal = self.env["account.journal"].search([("type", "=", "sale")], limit=1)
        for property in self:
            invoice = self.env['account.move'].create(
                {
                    "partner_id": property.buyer_id.id,
                    "move_type": "out_invoice",
                    "journal_id": journal.id,
                    "invoice_line_ids": [
                        Command.create({
                            "name": property.name,
                            "quantity": 1.0,
                            "price_unit": property.selling_price * 0.06,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1.0,
                            "price_unit": 100,
                        }),
                    ]
                }
            )
        return super().sold()




