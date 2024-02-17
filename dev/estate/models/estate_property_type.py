from odoo import fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "name desc"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many('estate.property', "property_type_id", string="property")

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'The property type must be unique.'),
    ]