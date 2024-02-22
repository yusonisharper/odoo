from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class EstatePropertyUser(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "user_id", domain=[("state", "in", ["new", "offer_received"])])