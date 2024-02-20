from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "estate property tag"
    _order = "name desc"

    name = fields.Char('Tag', required=True)
    color = fields.Integer('color')

    _sql_constraints = [
        ('check_property_tag', 'UNIQUE(name)', 'The property tag must be unique.'),
    ]