from odoo import fields, models

class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "estate property offer"
    _order = "id desc"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", copy=False, selection=[('accepted', 'Accepted'), ('refused', 'Refused')])
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
