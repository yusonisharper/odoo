from odoo import fields, models

class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "id desc"

    name = fields.Char('Tag', required=True)

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'The property tag must be unique.'),
    ]