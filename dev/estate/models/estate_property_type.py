from odoo import fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "id desc"

    name = fields.Char('Type', required=True)
