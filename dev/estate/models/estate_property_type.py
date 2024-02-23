from odoo import api, fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "estate property type"
    _order = "sequence,id"

    name = fields.Char('Type', required=True)
    property_ids = fields.One2many('estate.property', "property_type_id", string="property")
    sequence = fields.Integer('Sequence', default=1, help="Used to order type.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute='_compute_offer_count')

    _sql_constraints = [
        ('check_property_type', 'UNIQUE(name)', 'The property type must be unique.'),
    ]

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)